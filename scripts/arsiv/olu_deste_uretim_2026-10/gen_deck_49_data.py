import sys, os, json, re

# Deck 49 Data
def get_deck_49_spec():
    # 10 sections of 10 slides = 100 slides
    topics = []
    
    # helper to add a topic
    def add_t(title, subtitle, focus, lead, bullets, alert_text, summaries,
              cloze_s, cloze_t, cloze_h,
              tbl_title, tbl_headers, tbl_rows,
              chain_title, chain_steps,
              rec_q, rec_a,
              spot_topic, spot_items,
              quiz_q, quiz_opts, alert_type="NOTE"):
        topics.append({
            "title": title,
            "subtitle": subtitle,
            "clinical_focus": focus,
            "lead": lead,
            "bullets": bullets,
            "alert_type": alert_type,
            "alert_text": alert_text,
            "summaries": summaries,
            "cloze_sentence": cloze_s,
            "cloze_term": cloze_t,
            "cloze_hint": cloze_h,
            "table_title": tbl_title,
            "table_headers": tbl_headers,
            "table_rows": tbl_rows,
            "chain_title": chain_title,
            "chain_steps": chain_steps,
            "recall_q": rec_q,
            "recall_a": rec_a,
            "spot_topic": spot_topic,
            "spot_items": spot_items,
            "quiz_q": quiz_q,
            "quiz_opts": quiz_opts
        })

    # SECTION 1: Servisit Tanımı, Florası ve Bakteriyel Patojenler (1-10)
    # 1
    add_t(
        "Servisit Kavramı: Tanım ve Klinik Giriş",
        "Serviksin yaygın inflamatuvar tablosu ve klinik yansıması",
        "Tanım ve Epidemiyoloji",
        "Servisit, serviksin enfeksiyöz veya non-enfeksiyöz nedenlerle ortaya çıkan yangısal tablosudur. Kadın alt genital sisteminde polikliniklere başvuran hastalarda en sık karşılaşılan benign patolojilerin başında gelir.",
        [
            ("Mukozal Tutulum", "Servikal mukozada vasküler konjesyon, ödem ve epitel hasarı ile birlikte nötrofilik infiltrasyon gelişir."),
            ("Klinik Belirti", "Hastalarda sıklıkla pürülan veya mukopürülan nitelikte vajinal akıntı (lökore) ve zaman zaman temas kanaması izlenir."),
            ("Asendan Yayılım", "Uygun şekilde tedavi edilmeyen olgularda mikroorganizmalar üst genital yola yayılarak pelvik inflamatuvar hastalık riski doğurabilir.")
        ],
        "Servisit tek başına izole seyredebileceği gibi vajinit veya endometrit tablolarıyla kombine olarak da karşımıza çıkabilir.",
        ["Serviksin yaygın inflamatuvar durumudur.", "Mukopürülan akıntı en sık klinik belirtidir.", "Üst genital yola yayılım potansiyeli taşır."],
        "Serviksin mikrobiyal veya irritan etkenlerle gelişen yangısal sürecine servisit adı verilir.",
        "servisit", "Servikal dokunun yaygın yangısal antitesi",
        "Servisit Genel Klinik Özellikleri",
        ["Özellik", "Görülme Durumu", "Klinik Yansıması"],
        [
            {"cells": [{"text": "Prevalans", "isMasked": False}, {"text": "Son derece yaygın", "isMasked": True, "hint": "Toplumda yüksek sıklık"}, {"text": "Sık poliklinik başvurusu", "isMasked": False}]},
            {"cells": [{"text": "Klinik Seyir", "isMasked": False}, {"text": "Asemptomatik veya akıntılı", "isMasked": False}, {"text": "PİH gelişim riski", "isMasked": True, "hint": "Üst genital yayılım riski"}]}
        ],
        "Servisit Patogenezinin Başlangıç Aşamaları",
        [
            "1. Mukozal Temas: Mikroorganizma servikal kanala ve epitel yüzeyine yerleşir.",
            "2. Vasküler Yanıt: Stromadaki kılcal damarlarda belirgin konjesyon ve nötrofil göçü başlar.",
            "3. Sekresyon Artışı: Bezlerden ve hasarlı epitelden bol miktarda pürülan eksüda salgılanır.",
            "4. Semptom Başlangıcı: Hasta vajinal akıntı ve disparoni yakınmasıyla başvurur."
        ],
        "Servisit tablosunda hastayı doktora getiren en karakteristik jinekolojik yakınma nedir?",
        "Lökore olarak adlandırılan irinli veya mukopürülan vajinal akıntıdır.",
        "Servisitin Klinik ve Patolojik Temelleri",
        [
            {"text": "Servisit, serviksin jinekolojik pratikte en sık rastlanan inflamatuvar durumudur.", "isLie": False, "explanation": "Servikal inflamasyon kadın alt genital sisteminde en sık saptanan tablolardandır."},
            {"text": "Servisitte en tipik fizik muayene ve laboratuvar bulgusu mukopürülan vajinal akıntıdır.", "isLie": False, "explanation": "Mukopürülan eksüda ve lökore servisit için klasik bulgudur."},
            {"text": "Servisit daima malign bir karsinom sürecidir ve doğrudan kemik metastazı yapar.", "isLie": True, "explanation": "Tuzak! Servisit benign bir inflamasyondur, primer malign tümör değildir."},
            {"text": "Tedavi edilmeyen olgularda mikroorganizmalar asendan yolla üst genital traktusa yayılabilir.", "isLie": False, "explanation": "Asendan yolla endometrit, salpenjit ve pelvik inflamatuvar hastalık riski mevcuttur."}
        ],
        "Servisit tablosu ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
        [
            {"key": "A", "text": "Serviksin çok sık görülen benign inflamatuvar bir tablosudur", "isCorrect": True, "explanation": "Servisit benign yangısal bir antitedir ve en sık mukopürülan akıntıyla belirti verir."},
            {"key": "B", "text": "Yalnızca ileri evre invaziv skuamöz karsinom vakalarında ortaya çıkar", "isCorrect": False, "explanation": "Malignite şartı yoktur; çoğunlukla enfeksiyöz patojenlere bağlı selim süreçtir."},
            {"key": "C", "text": "Hiçbir zaman vajinal akıntıya veya lökoreye neden olmaz", "isCorrect": False, "explanation": "Aksine servisitin en tipik başvuru semptomu mukopürülan vajinal akıntıdır."},
            {"key": "D", "text": "Üst genital yola ilerleme veya pelvik inflamatuvar hastalık riski taşımaz", "isCorrect": False, "explanation": "Tedavi edilmediğinde mikroorganizmalar asendan yolla tüplere yayılabilir."}
        ]
    )

    print("Added slide 1. Total slides in spec:", len(topics))
    return topics

print("gen_deck_49_data loaded.")
