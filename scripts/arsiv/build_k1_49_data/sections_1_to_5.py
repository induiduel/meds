# Section 1 to 5 data generator for Deck 49 (Slides 1 to 50)
import json

def get_slides_1_to_50():
    slides = []
    
    # -------------------------------------------------------------
    # SECTION 1: Servisit Etyolojisi, Flora, Chlamydia ve HSV (Slides 1-10)
    # -------------------------------------------------------------
    
    # Slide 1
    slides.append({
        "slideNumber": 1,
        "title": "Servisit Kavramı: Tanım ve Klinik Giriş",
        "subtitle": "Serviksin yaygın inflamatuvar tablosu ve klinik yansıması",
        "clinicalFocus": "Tanım ve Epidemiyoloji",
        "content": "Servisit, kadın alt genital sisteminde serviksin inflamatuvar durumunu tanımlayan ve jinekolojik pratikte son derece sık karşılaşılan klinik bir antitedir. Rutin jinekolojik muayenelerde veya akıntı yakınmasıyla başvuran kadınlarda yüksek oranda saptanır.\n\n- **İnflamatuvar Karakter:** Servikal mukozanın enfeksiyöz patojenlerle veya mekanik/kimyasal etkenlerle uyarılması sonucu belirgin doku reaksiyonu ve vasküler konjesyon meydana gelir.\n- **Klinik Başvuru:** Olguların önemli bir kısmı asemptomatik seyrederken, semptomatik olgularda en sık rastlanan bulgu anormal vajinal akıntıdır.\n- **Halk Sağlığı Önemi:** Enfeksiyon tedavi edilmediğinde üst genital sisteme yayılarak pelvik inflamatuvar hastalık (PİH) ve infertilite riskini tetikleyebilir.\n\n> [!NOTE]\n> Servisit tek başına izole kalabileceği gibi vajinit veya endometrit tablolarıyla eş zamanlı birliktelik de gösterebilir.",
        "synthesisNarrative": "Servisit, kadın alt genital sisteminde serviksin inflamatuvar durumunu tanımlayan ve jinekolojik pratikte son derece sık karşılaşılan klinik bir antitedir. Rutin jinekolojik muayenelerde veya akıntı yakınmasıyla başvuran kadınlarda yüksek oranda saptanır.\n\n- **İnflamatuvar Karakter:** Servikal mukozanın enfeksiyöz patojenlerle veya mekanik/kimyasal etkenlerle uyarılması sonucu belirgin doku reaksiyonu ve vasküler konjesyon meydana gelir.\n- **Klinik Başvuru:** Olguların önemli bir kısmı asemptomatik seyrederken, semptomatik olgularda en sık rastlanan bulgu anormal vajinal akıntıdır.\n- **Halk Sağlığı Önemi:** Enfeksiyon tedavi edilmediğinde üst genital sisteme yayılarak pelvik inflamatuvar hastalık (PİH) ve infertilite riskini tetikleyebilir.\n\n> [!NOTE]\n> Servisit tek başına izole kalabileceği gibi vajinit veya endometrit tablolarıyla eş zamanlı birliktelik de gösterebilir.",
        "bulletPoints": [
            "Serviksin yaygın inflamatuvar sürecidir.",
            "Rutin muayenelerde veya akıntı şikayetiyle saptanır.",
            "Tedavi edilmediğinde üst genital sisteme yayılabilir."
        ],
        "relatedQuestions": [],
        "interactiveElements": [
            {
                "type": "cloze_masking",
                "sentence": "Serviksin inflamatuvar reaksiyonu ve doku yangısını tanımlayan klinik antiteye servisit adı verilir.",
                "maskedTerm": "servisit",
                "hint": "Servikal dokunun yaygın yangısal durumu"
            },
            {
                "type": "interactive_table",
                "tableTitle": "Servisit Genel Klinik Özellikleri",
                "tableHeaders": ["Klinik Parametre", "Görülme Şekli", "Klinik Önem"],
                "tableRows": [
                    {
                        "cells": [
                            {"text": "Prevalans", "isMasked": False},
                            {"text": "Oldukça yaygın", "isMasked": True, "hint": "Toplumda ve jinekolojide yüksek sıklık"},
                            {"text": "Poliklinik başvurularında sık", "isMasked": False}
                        ]
                    },
                    {
                        "cells": [
                            {"text": "Klinik Seyir", "isMasked": False},
                            {"text": "Asemptomatik veya akıntılı", "isMasked": False},
                            {"text": "PİH gelişim riski", "isMasked": True, "hint": "Üst genital trakt yayılım tehlikesi"}
                        ]
                    }
                ]
            },
            {
                "type": "causal_chain",
                "chainTitle": "Servisit Patogenezinin Başlangıç Aşamaları",
                "steps": [
                    "1. Mukozal Temas: Mikroorganizma veya irritan ajan servikal kanala ve ektoservikse ulaşır.",
                    "2. Epitel İnflamasyonu: Mukozal epitelde ödem, nötrofil infiltrasyonu ve vasküler konjesyon başlar.",
                    "3. Eksüda Oluşumu: İrinli veya mukopürülan sekresyon vajinal kanala boşalmaya başlar.",
                    "4. Klinik Yakınma: Hastada rahatsız edici akıntı veya temas kanaması şikayeti belirir."
                ]
            },
            {
                "type": "active_recall",
                "question": "Serviksin inflamatuvar durumuna ne ad verilir ve en sık hangi yakınmayla başvurulur?",
                "answer": "Servisit adı verilir; en sık anormal veya irinli vajinal akıntı yakınmasıyla doktora başvurulur."
            },
            {
                "type": "spot_the_lie",
                "topic": "Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Servisitin Genel Klinik Özellikleri",
                "items": [
                    {"text": "Servisit, serviksin kadın alt genital sisteminde en sık rastlanan inflamatuvar durumudur.", "isLie": False, "explanation": "Servisit jinekolojik pratikte en sık teşhis edilen servikal patolojilerdendir."},
                    {"text": "Semptomatik kadınlarda en yaygın başvuru bulgusu irinli vajinal akıntıdır.", "isLie": False, "explanation": "Mukopürülan akıntı servisitin en tipik semptomudur."},
                    {"text": "Servisit daima malign bir süreçtir ve kendiliğinden lenf nodu metastazı yapar.", "isLie": True, "explanation": "Tuzak! Servisit benign bir inflamasyondur, malign tümör veya primer lenf metastazı değildir."},
                    {"text": "Tedavi edilmeyen olgularda mikroorganizmalar üst genital yola yayılarak pelvik inflamatuvar hastalık riski doğurabilir.", "isLie": False, "explanation": "Asendan yolla endometrit ve salpenjit gelişme riski mevcuttur."}
                ]
            },
            {
                "type": "micro_quiz",
                "question": "Servisit tablosu ile ilgili aşağıdaki klinik ifadelerden hangisi DOĞRUDUR?",
                "microQuizOptions": [
                    {
                        "key": "A",
                        "text": "Serviksin çok sık görülen benign inflamatuvar bir tablosudur",
                        "isCorrect": True,
                        "explanation": "Servisit servikal dokunun yaygın yangısı olup sıklıkla enfeksiyöz kökenlidir."
                    },
                    {
                        "key": "B",
                        "text": "Yalnızca ileri evre invaziv skuamöz karsinom zemininde ortaya çıkar",
                        "isCorrect": False,
                        "explanation": "Malignite şartı yoktur; çoğunlukla enfeksiyöz ajanların yol açtığı benign tablodur."
                    },
                    {
                        "key": "C",
                        "text": "Hiçbir zaman vajinal akıntı veya pürülan sekresyona yol açmaz",
                        "isCorrect": False,
                        "explanation": "Aksine servisitin en tipik semptomu mukopürülan ve irinli vajinal akıntıdır."
                    },
                    {
                        "key": "D",
                        "text": "Üst genital traktusa ilerleme veya pelvik inflamatuvar hastalık oluşturma riski yoktur",
                        "isCorrect": False,
                        "explanation": "Özellikle klamidyal ve gonokokal servisitler asendan yayılımla PİH yapabilir."
                    }
                ]
            }
        ]
    })
    
    return slides

print("Section 1-5 generator template loaded.")
