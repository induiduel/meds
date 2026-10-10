# Multi-part generator for Deck 49
import json, os, sys, re

DECK_ID = 'k1p-k1-49-invaziv-serviks-kanseri-ve-endometriyozis'

def fold(s):
    return str(s or '').lower().replace('ı', 'i').replace('İ', 'i')

def leaks(hint, answer):
    h = fold(hint)
    return any((w[:5] if len(w) > 5 else w) in h for w in re.findall(r'[\wçğıöşü%.,-]+', fold(answer)) if len(w) >= 3 or re.search(r'\d', w))

def check_slide(s):
    items = s.get('interactiveElements', [])
    if len(items) < 4 or len(items) > 6:
        raise ValueError(f'Slide {s.get("slideNumber")} has {len(items)} items; expected 4-6.')
    for e in items:
        t = e.get('type')
        if t == 'feature_bidding':
            raise ValueError('feature_bidding is forbidden!')
        if t == 'cloze_masking':
            sen = e.get('sentence', '')
            term = e.get('maskedTerm', '')
            hint = e.get('hint', '')
            if not term or fold(term) not in fold(sen):
                raise ValueError(f'Slide {s.get("slideNumber")} cloze term {term!r} not in {sen!r}')
            if hint and leaks(hint, term):
                raise ValueError(f'Slide {s.get("slideNumber")} cloze hint leak: {hint!r} -> {term!r}')
        elif t == 'interactive_table':
            headers = e.get('tableHeaders', [])
            for row in e.get('tableRows', []):
                cells = row.get('cells', [])
                if len(cells) != len(headers):
                    raise ValueError(f'Slide {s.get("slideNumber")} table row length mismatch')
                for c in cells:
                    if c.get('isMasked') and c.get('hint') and leaks(c.get('hint'), c.get('text')):
                        raise ValueError(f'Slide {s.get("slideNumber")} table hint leak: {c.get("hint")!r} -> {c.get("text")!r}')
        elif t == 'spot_the_lie':
            topic = e.get('topic', '')
            if not topic:
                raise ValueError(f'Slide {s.get("slideNumber")} spot_the_lie missing topic')
            its = e.get('items', [])
            lies = [i for i in its if i.get('isLie')]
            if len(lies) != 1:
                raise ValueError(f'Slide {s.get("slideNumber")} spot_the_lie must have exactly 1 lie')
            for it in its:
                if not it.get('explanation'):
                    raise ValueError(f'Slide {s.get("slideNumber")} spot_the_lie item missing explanation')
        elif t == 'micro_quiz':
            opts = e.get('microQuizOptions', [])
            corr = [o for o in opts if o.get('isCorrect')]
            if len(corr) != 1:
                raise ValueError(f'Slide {s.get("slideNumber")} micro_quiz must have exactly 1 correct option')
            for o in opts:
                if not o.get('explanation'):
                    raise ValueError(f'Slide {s.get("slideNumber")} micro_quiz option missing explanation')

print('Validation helper is solid.')

def build_deck_49_slides():
    slides = []
    
    # -------------------------------------------------------------
    # SECTION 1 (Slides 1-10): Servisit, Mikrobiyota, Patojenler ve Erozyon
    # -------------------------------------------------------------
    
    # Slide 1: Servisit Tanımı ve Flora
    s1 = {
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
                            {"text": "Mukopürülan eksüda ve lökore", "isMasked": True, "hint": "Servikal kanaldan gelen iltihabi salgı"},
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
    check_slide(s1)
    slides.append(s1)
    return slides

print('Slide 1 added and validated successfully!')
