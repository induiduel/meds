import json

def get_section_1():
    slides = [
        # S1
        {
            "slideNumber": 1,
            "title": "Kadın Alt Genital Sistemi: Vulvanın Anatomik ve Histolojik Çerçevesi",
            "subtitle": "Kıllı deri ve mukozal yüzeylerin histolojik organizasyonu",
            "clinicalFocus": "Anatomi ve Histoloji",
            "content": "Vulva, dış kadın genital organlarını tanımlayan ve hem keratinize çok katlı yassı epitel içeren kıl foliküllü deriyi hem de nemli mukozal yüzeyleri bir arada barındıran anatomik bölgedir. Bu iki farklı doku mimarisi, gelişebilecek patolojilerin karakterini ve klinik seyrini doğrudan belirler.

- **Kıllı Deri Örtüsü:** Labia majora, tipik kıl folikülleri, yağ bezleri ve apokrin ter bezleri barındıran keratinize epidermis ile kaplıdır; dermatolojik lezyonlar sıklıkla bu alana yerleşir.
- **Mukozal Yüzeyler:** Labia minora, klitoris ve vestibül nemli, keratinize olmayan veya hafif keratinize çok katlı yassı epitelle döşelidir; kıl folikülü içermez ve kimyasal irritanlara karşı oldukça geçirgendir.
- **Hastalık Spektrumu:** En sık karşılaşılan tablolar hafif veya rahatsız edici inflamatuvar lezyonlardır; malign tümörler ise nadir görülmekle birlikte hayatı tehdit edici potansiyele sahiptir.

> [!NOTE]
> Vulva lezyonlarında lezyonun kıl folikülü içeren labia majorada mı yoksa mukozal labia minorada mı yerleştiği ayırıcı tanıda yol göstericidir.",
            "synthesisNarrative": "Vulva, dış kadın genital organlarını tanımlayan ve hem keratinize çok katlı yassı epitel içeren kıl foliküllü deriyi hem de nemli mukozal yüzeyleri bir arada barındıran anatomik bölgedir. Bu iki farklı doku mimarisi, gelişebilecek patolojilerin karakterini ve klinik seyrini doğrudan belirler.

- **Kıllı Deri Örtüsü:** Labia majora, tipik kıl folikülleri, yağ bezleri ve apokrin ter bezleri barındıran keratinize epidermis ile kaplıdır; dermatolojik lezyonlar sıklıkla bu alana yerleşir.
- **Mukozal Yüzeyler:** Labia minora, klitoris ve vestibül nemli, keratinize olmayan veya hafif keratinize çok katlı yassı epitelle döşelidir; kıl folikülü içermez ve kimyasal irritanlara karşı oldukça geçirgendir.
- **Hastalık Spektrumu:** En sık karşılaşılan tablolar hafif veya rahatsız edici inflamatuvar lezyonlardır; malign tümörler ise nadir görülmekle birlikte hayatı tehdit edici potansiyele sahiptir.

> [!NOTE]
> Vulva lezyonlarında lezyonun kıl folikülü içeren labia majorada mı yoksa mukozal labia minorada mı yerleştiği ayırıcı tanıda yol göstericidir.",
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
                                {"text": "Labia majora", "isMasked": false},
                                {"text": "Keratinize çok katlı yassı epitel", "isMasked": false},
                                {"text": "kıl folikülü ve apokrin ter bezleri", "isMasked": true, "hint": "deri ekleri"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Labia minora", "isMasked": false},
                                {"text": "Keratinize olmayan mukoza", "isMasked": true, "hint": "nemli mukoza katmanı"},
                                {"text": "Kıl folikülü bulunmaz", "isMasked": false}
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
                        {"text": "Labia majora, kıl folikülü ve yağ bezleri içeren keratinize deri örtüsünden oluşur.", "isLie": false, "explanation": "Labia majora tipik dış kıl örtüsü ve apokrin/ekrin bezleri barındıran deri katmanıdır."},
                        {"text": "Labia minora mukozal yapıda olup kıl folikülü içermeyen çok katlı yassı epitelle döşelidir.", "isLie": false, "explanation": "Labia minora mukoza karakterindedir ve kıl folikülü barındırmaz."},
                        {"text": "Vulvada en sık karşılaşılan lezyonlar inflamatuvar süreçlerdir; maligniteler daha nadirdir.", "isLie": false, "explanation": "İnflamatuvar tablolar vulvanın en sık hastalığıdır, kanserler nadirdir."},
                        {"text": "Labia minora yoğun kıl folikülleriyle kaplı kalın keratinize deri yapısındadır.", "isLie": true, "explanation": "Tuzak! Kıl folikülleri labia minorada değil, labia majorada bulunur; labia minora mukozal yapıdadır."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Vulva anatomisi ve doku katmanları ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Labia majora kıl folikülü ve ek bezler içeren keratinize çok katlı yassı epitelle döşelidir",
                            "isCorrect": true,
                            "explanation": "Labia majora dış genital bölgenin kıllı deri örtüsünü oluşturur ve tipik deri eklerini barındırır."
                        },
                        {
                            "key": "B",
                            "text": "Labia minora yoğun kıl folikülü içeren kalın bir epidermis tabakasına sahiptir",
                            "isCorrect": false,
                            "explanation": "Labia minora mukozal karakterdedir ve kıl folikülü kesinlikle içermez."
                        },
                        {
                            "key": "C",
                            "text": "Vulvada malign tümörler inflamatuvar lezyonlardan çok daha sık izlenir",
                            "isCorrect": false,
                            "explanation": "Tam tersine en sık patolojiler inflamatuvar karakterdedir; maligniteler oldukça nadirdir."
                        },
                        {
                            "key": "D",
                            "text": "Vulvanın hiçbir bölgesinde keratinize çok katlı yassı epitel yer almaz",
                            "isCorrect": false,
                            "explanation": "Labia majora tam aksine keratinize çok katlı yassı deri epitelinden oluşur."
                        }
                    ]
                }
            ]
        }
    ]
    return slides
