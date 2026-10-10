import sys, os, json, re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from meds.scripts.apply_generated_deck import apply_deck
from meds.scripts.generate_deck_core import sanitize_deck
from meds.scripts.generate_deck_util import make_slide
from meds.scripts.build_deck_49_generator import get_deck_49_flashcards

DECK_ID = "k1p-k1-49-invaziv-serviks-kanseri-ve-endometriyozis"

# Generator for 100 slides broken down into 10 structured sections
def generate_100_slides():
    slides = []
    
    # -------------------------------------------------------------------------
    # SECTION 1: Servisit Etyolojisi, Vajinal Flora ve Patojenler (Slayt 1 - 10)
    # -------------------------------------------------------------------------
    # Slayt 1
    slides.append(make_slide(
        slide_num=1,
        title="Servisit Kavramı: Tanım ve Klinik Giriş",
        subtitle="Serviksin yaygın inflamatuvar tablosu ve klinik yansıması",
        clinical_focus="Tanım ve Epidemiyoloji",
        lead_paragraph="Servisit, serviks dokusunun mikrobiyal etkenler, kimyasal irritanlar veya travmatik faktörler zemininde gelişen yaygın inflamatuvar tablosudur. Kadın alt genital sisteminde jinekolojik polikliniklere en sık başvuru gerektiren temel antiteler arasında yer alır.",
        bullet_tuples=[
            ("Mukozal Tutulum", "Servikal kanalı döşeyen silindirik epitel veya ektoservikal çok katlı yassı epitel yangısal yanıta katılır; konjesyon ve nötrofil göçü belirgindir."),
            ("Klinik Tablo", "Hastalarda sıklıkla pürülan veya mukopürülan nitelikte vajinal akıntı (lökore) ve zaman zaman temas kanaması ortaya çıkar."),
            ("Asendan Yayılım Riski", "Uygun şekilde tedavi edilmeyen enfeksiyonlar endometrium ve fallop tüplerine ilerleyerek pelvik inflamatuvar hastalık oluşturabilir.")
        ],
        alert_type="NOTE",
        alert_text="Servisit tek başına izole seyredebileceği gibi, vajinit veya üst genital yol enfeksiyonlarıyla kombine olarak da karşımıza çıkabilir.",
        bullet_summaries=[
            "Serviksin yaygın inflamatuvar tablosudur.",
            "Mukopürülan akıntı en sık klinik belirtidir.",
            "Üst genital yola yayılarak PİH riski oluşturabilir."
        ],
        interactive_items=[
            {
                "type": "cloze_masking",
                "sentence": "Serviksin mikrobiyal veya irritan etkenlerle gelişen yangısal sürecine servisit adı verilir.",
                "maskedTerm": "servisit",
                "hint": "Servikal dokunun yaygın inflamasyonu"
            },
            {
                "type": "interactive_table",
                "tableTitle": "Servisit Temel Patolojik Parametreleri",
                "tableHeaders": ["Parametre", "Gözlenen Durum", "Klinik Yansıması"],
                "tableRows": [
                    {
                        "cells": [
                            {"text": "İnflamasyon Yeri", "isMasked": False},
                            {"text": "Servikal mukoza ve stroma", "isMasked": True, "hint": "Serviksin anatomik doku katmanı"},
                            {"text": "Eritem ve ödem gelişir", "isMasked": False}
                        ]
                    },
                    {
                        "cells": [
                            {"text": "Majör Belirti", "isMasked": False},
                            {"text": "Mukopürülan akıntı", "isMasked": True, "hint": "İrinli vajinal sekresyon"},
                            {"text": "Lökore tablosu", "isMasked": False}
                        ]
                    }
                ]
            },
            {
                "type": "causal_chain",
                "chainTitle": "Servisit Gelişim Basamakları",
                "steps": [
                    "1. Mukozal Ajan Girişi: Enfeksiyöz patojen servikal kanala ve epitel yüzeyine yerleşir.",
                    "2. Vasküler Yanıt: Stromadaki kılcal damarlarda belirgin konjesyon ve nötrofil göçü başlar.",
                    "3. Sekresyon Artışı: Bezlerden ve hasarlı epitelden bol miktarda pürülan eksüda salgılanır.",
                    "4. Semptom Başlangıcı: Hasta vajinal akıntı ve disparoni yakınmasıyla başvurur."
                ]
            },
            {
                "type": "active_recall",
                "question": "Servisit tablosunda hastayı doktora getiren en karakteristik jinekolojik yakınma nedir?",
                "answer": "Mukopürülan ve irinli vajinal akıntıdır (lökore)."
            },
            {
                "type": "spot_the_lie",
                "topic": "Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Servisitin Klinik ve Patolojik Temelleri",
                "items": [
                    {"text": "Servisit, servikal dokunun jinekolojik pratikte en sık rastlanan inflamatuvar durumudur.", "isLie": False, "explanation": "Servikal inflamasyon jinekolojide son derece yaygın bir tanıdır."},
                    {"text": "Servisitte en tipik fizik muayene ve laboratuvar bulgusu mukopürülan vajinal akıntıdır.", "isLie": False, "explanation": "Mukopürülan sekresyon ve lökore servisit için klasik bulgulardır."},
                    {"text": "Servisit daima malign bir süreçtir ve kendiliğinden kemik metastazı yapar.", "isLie": True, "explanation": "Tuzak! Servisit benign bir inflamatuvar hastalıktır, metastaz yapmaz."},
                    {"text": "Tedavi edilmeyen servisit olgularında mikroorganizmalar asendan yolla üst genital traktusa yayılabilir.", "isLie": False, "explanation": "Enfeksiyon endometrium ve tüplere ilerleyerek PİH oluşturabilir."}
                ]
            },
            {
                "type": "micro_quiz",
                "question": "Servisit tablosunun genel patolojik ve klinik seyri ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                "microQuizOptions": [
                    {
                        "key": "A",
                        "text": "Serviksin sık görülen benign inflamatuvar bir tablosudur ve mukopürülan akıntı yapabilir",
                        "isCorrect": True,
                        "explanation": "Servikal dokunun yangısı olup en karakteristik belirtisi mukopürülan lökoredir."
                    },
                    {
                        "key": "B",
                        "text": "Yalnızca ileri evre invaziv skuamöz karsinom vakalarında ortaya çıkan bir lezyondur",
                        "isCorrect": False,
                        "explanation": "Malignite şartı yoktur; çoğunlukla enfeksiyöz ajanların yol açtığı selim süreçtir."
                    },
                    {
                        "key": "C",
                        "text": "Hiçbir zaman vajinal akıntıya veya epitelde ödeme neden olmaz",
                        "isCorrect": False,
                        "explanation": "Aksine inflamasyonla birlikte ödem, vasküler konjesyon ve pürülan akıntı gelişir."
                    },
                    {
                        "key": "D",
                        "text": "Üst genital traktusa ilerleme veya pelvik inflamatuvar hastalık tablosuna yol açma riski yoktur",
                        "isCorrect": False,
                        "explanation": "Asendan yolla pelvik inflamatuvar hastalık ve buna bağlı infertilite riski taşır."
                    }
                ]
            }
        ]
    ))

    # We will build the remaining slides modularly
    return slides

print("Runner loaded.")
