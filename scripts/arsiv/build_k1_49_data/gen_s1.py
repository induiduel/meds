# Section 1 for Deck 49 (Slides 1-10)
import json

def get_s1_slides():
    slides = [
        {
            "slideNumber": 1,
            "title": "Servisit: Tanım, Akıntı Tipleri ve Normal Vajinal Flora",
            "subtitle": "Alt genital yolun yangısal tablosu ve kommensal mikrobiyota dengesi",
            "clinicalFocus": "Servisit Tanımı ve Flora",
            "content": "Servisit, serviks uteri dokusunun enfeksiyöz veya enfeksiyöz olmayan etkenlerle gelişen yaygın inflamatuvar durumudur. Klinik pratikte en sık rastlanan jinekolojik tablolardan biridir.

- **Klinik Başvuru:** Servisit olguları sıklıkla belirgin irinli (pürülan) veya mukopürülan vajinal akıntı ve lökore ile prezante olur.
- **Vajinal Flora Zorluğu:** Vajen ve servikste yerleşik yoğun bir mikrobiyota bulunur. Bu nedenle enfeksiyonlu servisit ile enfeksiyon dışı irritan inflamasyonun kesin ayrımı mikrobiyolojik olarak güçtür.
- **Normal Vajinal Flora Elemanları:** Aerob ve anaerob bakteriler, Streptococcus türleri, Staphylococcus türleri, Enterococcus türleri, Escherichia coli ve Candida türleri tesadüfi kommensal elemanlar olarak bulunabilir.

> [!NOTE]
> Normal vajinal florada bulunan mikroorganizmalar konağın immünitesi bozulmadıkça doku hasarı yapmaz; ancak servisit ayırıcı tanısında kafa karışıklığı yaratabilir.",
            "synthesisNarrative": "Servisit, serviks uteri dokusunun enfeksiyöz veya enfeksiyöz olmayan etkenlerle gelişen yaygın inflamatuvar durumudur. Klinik pratikte en sık rastlanan jinekolojik tablolardan biridir.

- **Klinik Başvuru:** Servisit olguları sıklıkla belirgin irinli (pürülan) veya mukopürülan vajinal akıntı ve lökore ile prezante olur.
- **Vajinal Flora Zorluğu:** Vajen ve servikste yerleşik yoğun bir mikrobiyota bulunur. Bu nedenle enfeksiyonlu servisit ile enfeksiyon dışı irritan inflamasyonun kesin ayrımı mikrobiyolojik olarak güçtür.
- **Normal Vajinal Flora Elemanları:** Aerob ve anaerob bakteriler, Streptococcus türleri, Staphylococcus türleri, Enterococcus türleri, Escherichia coli ve Candida türleri tesadüfi kommensal elemanlar olarak bulunabilir.

> [!NOTE]
> Normal vajinal florada bulunan mikroorganizmalar konağın immünitesi bozulmadıkça doku hasarı yapmaz; ancak servisit ayırıcı tanısında kafa karışıklığı yaratabilir.",
            "bulletPoints": [
                "Servisit serviksin yaygın inflamasyonudur.",
                "Sıklıkla irinli ve mukopürülan vajinal akıntı eşlik eder.",
                "Vajinal flora ayrımı zorlaştırabilir."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Servisit olgularında hastalar en sık irinli vajinal akıntı ve lökore şikayeti ile başvurur.",
                    "maskedTerm": "irinli vajinal akıntı",
                    "hint": "Pürülan karakterde genital eksüda tablosu"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Servisit ve Vajinal Mikrobiyota Elemanları",
                    "tableHeaders": ["Kategori", "Örnek Mikroorganizmalar", "Klinik Önemi"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Normal Flora", "isMasked": False},
                                {"text": "Streptococcus, Staphylococcus, E. coli, Candida", "isMasked": False},
                                {"text": "Fırsatçı üreme potansiyeli taşır", "isMasked": True, "hint": "Konak direnci düştüğünde patojenleşme riski"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Servisit Bulgusu", "isMasked": False},
                                {"text": "Mukopürülan eksüda ve lökore", "isMasked": True, "hint": "Servikal kanaldan gelen iltihabi akıntı"},
                                {"text": "Eritematöz ve ödemli endoserviks", "isMasked": False}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Flora Dengesinden Servisite",
                    "steps": [
                        "1. Flora Dengesi: Vajen ve serviks laktobasiller ve kommensal bakterilerle dengede tutulur.",
                        "2. Bariyer Bozulması: Fiziksel travma, kimyasal temas veya hormonal dalgalanmalar servikal mukozayı zedeler.",
                        "3. Nötrofil Göçü: İnflamatuvar uyarıyla birlikte servikal stromaya ve lümene yoğun polimorf lökosit göçer.",
                        "4. Akıntı Oluşumu: İrinli eksüda servikal kanaldan vajinaya dökülerek mukopürülan akıntı yaratır."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Servisitte enfeksiyonlu ve enfeksiyon dışı ayrımının klinik olarak zor olmasının temel nedeni nedir?",
                    "answer": "Vajinal florada Streptococcus, Staphylococcus, Enterococcus, E. coli ve Candida gibi çok sayıda kommensal mikroorganizmanın doğal olarak bulunmasıdır."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Servisit Tanımı ve Vajinal Flora İlişkisi: Aşağıdaki klinik ve mikrobiyolojik önermelerden hangisi yanlıştır (tuzaktır)?",
                    "items": [
                        {"text": "Servisit serviksin sık görülen inflamasyonudur ve sıklıkla irinli akıntıyla seyreder.", "isLie": False, "explanation": "Servisit tablosunun en tipik dışavurumu mukopürülan veya irinli lökoredir."},
                        {"text": "Vajinal florada aerob ve anaerob bakteriler tesadüfi eleman olarak yer alabilir.", "isLie": False, "explanation": "Normal vajinal mikrobiyota çeşitli kommensal bakteri türlerini barındırır."},
                        {"text": "E. coli ve Candida türleri vajinal florada bulunabilen mikroorganizmalardandır.", "isLie": False, "explanation": "Bu mikroorganizmalar asemptomatik kadınların florasında da saptanabilir."},
                        {"text": "Servisit tanısı alan her olguda vajinal flora tamamen yok olmuştur ve hiçbir bakteri saptanamaz.", "isLie": True, "explanation": "Tuzak! Tam aksine vajinal floranın varlığı enfeksiyonlu ve enfeksiyon dışı servisit ayrımını güçleştiren temel faktördür."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Servisit patofizyolojisi ve vajinal flora ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Servisit sıklıkla irinli vajinal akıntı ile seyreder ve vajinal flora nedeniyle enfeksiyonlu ayrımı zor olabilir",
                            "isCorrect": True,
                            "explanation": "Mukopürülan akıntı en belirgin bulgudur ve geniş kommensal flora spesifik ayrımı güçleştirir."
                        },
                        {
                            "key": "B",
                            "text": "Servisit daima tek bir protozoonun invazyonu ile tetiklenen nadir bir tablodur",
                            "isCorrect": False,
                            "explanation": "Servisit çok yaygındır ve bakteriyel, viral, fungal veya non-enfeksiyöz pek çok etkene bağlıdır."
                        },
                        {
                            "key": "C",
                            "text": "Normal vajinal florada hiçbir zaman mantar veya E. coli gibi bakteriler bulunamaz",
                            "isCorrect": False,
                            "explanation": "Candida türleri ve E. coli vajinal florada tesadüfi kommensal olarak yer alabilir."
                        },
                        {
                            "key": "D",
                            "text": "Servisitte inflamasyon yalnızca ektoservikse sınırlıdır ve endoservikal kanal asla etkilenmez",
                            "isCorrect": False,
                            "explanation": "Endoservikal kanal ve kolumnar bezler servisitin primer tutulum alanlarındandır."
                        }
                    ]
                }
            ]
        }
    ]
    return slides
