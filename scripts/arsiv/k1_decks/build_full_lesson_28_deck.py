# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 28: Tümör Biyolojisi ve Terminolojisi
(Prof. Dr. Hikmet Keleş - Tıbbi Patoloji ABD)
Master Deck Oluşturucu ve Multi-Format Paketleyici.

- 10 Bölüm, 100 Slayt, 10 Checkpoint
- 30 Akıl Kartı (Her checkpoint'te 3 adet, 0 hint leak)
- 7 İnteraktif Eleman Tipi (Her biri >= %8.0 çeşitlilik)
- Multi-format paketleme: manifest.json, content.md, blocks.html, structure.xml
- Runtime item: meds/src/data/decks/items/k1p-k1-28-tumor-biyolojisi-ve-terminolojisi.json
- Yerinde güncelleme: interactive_learning_decks.json (indeks 75) ve catalog.json (indeks 75)
"""

import os
import sys
import json
import re
import xml.etree.ElementTree as ET
from xml.dom import minidom
from collections import Counter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from scripts.k1_28_deck_data.section_1 import get_section_1_slides
from scripts.k1_28_deck_data.section_2 import get_section_2_slides
from scripts.k1_28_deck_data.section_3 import get_section_3_slides
from scripts.k1_28_deck_data.section_4 import get_section_4_slides
from scripts.k1_28_deck_data.section_5 import get_section_5_slides
from scripts.k1_28_deck_data.section_6 import get_section_6_slides
from scripts.k1_28_deck_data.section_7 import get_section_7_slides
from scripts.k1_28_deck_data.section_8 import get_section_8_slides
from scripts.k1_28_deck_data.section_9 import get_section_9_slides
from scripts.k1_28_deck_data.section_10 import get_section_10_slides
from scripts.enrich_k1_28_elements import enrich_slides

MEDS_DIR = os.path.join(BASE_DIR, "meds")
QUESTIONS_FILE = os.path.join(MEDS_DIR, "src/data/ornek_sorular/k1/k1-28-tumor-biyolojisi-ve-terminolojisi.json")
PACKAGE_DIR = os.path.join(MEDS_DIR, "src/data/decks/packages/k1p-k1-28-tumor-biyolojisi-ve-terminolojisi")
DECKS_ITEMS_DIR = os.path.join(MEDS_DIR, "src/data/decks/items")
INTERACTIVE_DECKS_PATH = os.path.join(MEDS_DIR, "src/data/interactive_learning_decks.json")
CATALOG_PATH = os.path.join(MEDS_DIR, "src/data/decks/catalog.json")

def leaks(hint, answer):
    if not hint or not answer:
        return False
    h = hint.lower().strip()
    a = answer.lower().strip()
    hw = set(re.findall(r'\b[a-zçğıöşü]{4,}\b', h))
    aw = set(re.findall(r'\b[a-zçğıöşü]{4,}\b', a))
    return bool(hw & aw)

def prettify_xml(elem):
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def build_lesson_28_deck():
    print("=" * 60)
    print("KURUL 1 - DERS 28: TÜMÖR BİYOLOJİSİ VE TERMİNOLOJİSİ")
    print("MASTER DECK VE MULTI-FORMAT PAKETLEME")
    print("=" * 60)

    # 1. 10 BÖLÜMÜN SLAYTLARINI TOPLA (100 SLAYT)
    raw_slides = (
        get_section_1_slides() + get_section_2_slides() + get_section_3_slides() +
        get_section_4_slides() + get_section_5_slides() + get_section_6_slides() +
        get_section_7_slides() + get_section_8_slides() + get_section_9_slides() +
        get_section_10_slides()
    )
    assert len(raw_slides) == 100, f"HATA: Toplam slayt sayısı 100 olmalıdır! Bulunan: {len(raw_slides)}"
    print(f"1. 10 Bölümden toplam {len(raw_slides)} slayt başarıyla toplandı.")

    # 2. ÖRNEK SORULARI YÜKLE
    questions = []
    if os.path.exists(QUESTIONS_FILE):
        with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
            q_data = json.load(f)
        raw_list = []
        if isinstance(q_data, dict):
            for k_item in q_data.get("kazanimlar", []):
                for q_item in k_item.get("sorular", []):
                    raw_list.append(q_item)
            if not raw_list and "sorular" in q_data:
                raw_list = q_data["sorular"]
        elif isinstance(q_data, list):
            raw_list = q_data

        for q in raw_list:
            q_id = q.get("id") or f"k1-28-q{len(questions)+1:02d}"
            q_text = q.get("soru") or q.get("question", "")
            raw_opts = q.get("secenekler") or q.get("options", {})
            corr = q.get("dogru") or q.get("correctAnswer", "A")
            if isinstance(corr, str) and len(corr) > 1 and corr[0] in "ABCDE":
                corr = corr[0]
            gen_exp = q.get("aciklama") or q.get("explanation", "")
            opt_exps = q.get("sik_aciklamalari") or {}

            normalized_opts = []
            if isinstance(raw_opts, dict):
                for k_opt in sorted(raw_opts.keys()):
                    txt_opt = raw_opts[k_opt]
                    exp_opt = opt_exps.get(k_opt) or (f"Doğru cevap {k_opt}'dir: {gen_exp}" if k_opt == corr else f"{k_opt} seçeneği yanlıştır.")
                    normalized_opts.append({
                        "key": k_opt,
                        "text": txt_opt,
                        "explanation": exp_opt
                    })
            elif isinstance(raw_opts, list):
                for idx, o in enumerate(raw_opts):
                    k_opt = chr(ord('A') + idx)
                    if isinstance(o, dict):
                        txt_opt = o.get("text", "")
                        exp_opt = o.get("explanation", f"{k_opt} seçeneği {'doğrudur' if k_opt == corr else 'yanlıştır'}.")
                    else:
                        txt_opt = str(o)
                        exp_opt = f"Doğru cevap {k_opt}'dir: {gen_exp}" if k_opt == corr else f"{k_opt} seçeneği yanlıştır."
                    normalized_opts.append({
                        "key": k_opt,
                        "text": txt_opt,
                        "explanation": exp_opt
                    })

            questions.append({
                "id": q_id,
                "question": q_text,
                "options": normalized_opts,
                "correctAnswer": corr,
                "explanation": gen_exp
            })
    print(f"2. {len(questions)} adet örnek soru başarıyla yüklendi ve normalize edildi.")

    # 3. SLAYTLARI STANDARTLAŞTIR VE ZENGİNLEŞTİR
    standardized_slides = []
    checkpoint_cards_map = {}

    for idx, s in enumerate(raw_slides):
        slide_num = idx + 1
        title = s.get("title", f"Slayt {slide_num}")
        content = s.get("content") or s.get("narrative", "")
        raw_elements = s.get("elements") or s.get("interactiveElements") or []

        # Checkpoint akıl kartlarını ayır
        fcs = s.get("flashcards") or [el for el in raw_elements if isinstance(el, dict) and "front" in el]
        if fcs:
            checkpoint_cards_map[slide_num] = fcs

        clean_elements = [el for el in raw_elements if isinstance(el, dict) and el.get("type")]

        standardized_slides.append({
            "id": f"k1-28-s{slide_num:02d}",
            "slideNumber": slide_num,
            "title": title,
            "content": content,
            "sourcePdf": s.get("sourcePdf", "Tıbbi Patoloji ABD - Tümör Biyolojisi ve Terminolojisi (Prof. Dr. Hikmet Keleş)"),
            "elements": clean_elements
        })

    # enrich_slides ile %8+ çeşitliliği sağla
    for s in standardized_slides:
        s["interactiveElements"] = s["elements"]

    enriched_slides = enrich_slides(standardized_slides)
    for s in enriched_slides:
        s["elements"] = s["interactiveElements"]
        if "interactiveElements" in s:
            del s["interactiveElements"]

    element_counts = Counter()
    for s in enriched_slides:
        for el in s.get("elements", []):
            element_counts[el.get("type")] += 1

    total_elements = sum(element_counts.values())
    print(f"3. İnteraktif elemanlar dengelendi (Toplam: {total_elements}):")
    for el_type, count in sorted(element_counts.items()):
        ratio = (count / total_elements) * 100
        print(f"   - {el_type}: {count} adet (%{ratio:.2f})")
        assert ratio >= 8.0, f"HATA: {el_type} oranı %8'in altında (%{ratio:.2f})!"

    # 4. CHECKPOINTLERE 30 AKIL KARTINI EKLE
    all_flashcards = []
    checkpoint_indices = [9, 19, 29, 39, 49, 59, 69, 79, 89, 100]

    for cp_num in checkpoint_indices:
        slide_idx = cp_num - 1
        s = enriched_slides[slide_idx]
        cards = checkpoint_cards_map.get(cp_num, [])
        assert len(cards) == 3, f"HATA: Slayt {cp_num} için 3 akıl kartı olmalı, {len(cards)} var!"
        s["flashcards"] = cards
        all_flashcards.extend(cards)

    print(f"4. 10 Checkpoint'e toplam {len(all_flashcards)} akıl kartı eklendi (Her checkpoint'te 3 adet).")

    # Hint sızıntısı kontrolü
    leak_count = 0
    for fc in all_flashcards:
        if leaks(fc.get("hint", ""), fc.get("back", "")):
            leak_count += 1
            print(f"   UYARI: Hint sızıntısı tespit edildi: {fc['id']} -> {fc['hint']} (Cevap: {fc['back']})")
    assert leak_count == 0, f"HATA: Toplam {leak_count} akıl kartında ipucu sızıntısı var!"
    print("   Akıl kartı ipucu sızıntı kontrolü: 0 SIZINTI (KUSURSUZ).")

    # 5. DECK VERİ YAPISINI HAZIRLA
    deck_data = {
        "id": "k1p-k1-28-tumor-biyolojisi-ve-terminolojisi",
        "title": "Tümör Biyolojisi ve Terminolojisi",
        "subtitle": "Neoplazi İlkeleri, Benign/Malign Ayrımı, İsimlendirme, Mikst/Blastik Tümörler, Diferansiyasyon/Anaplazi, Lokal İnvazyon, Metastaz, Epidemiyoloji ve Moleküler Karsinogenez",
        "slug": "k1p-k1-28-tumor-biyolojisi-ve-terminolojisi",
        "description": "Prof. Dr. Hikmet Keleş (Tıbbi Patoloji ABD) tarafından hazırlanan Tümör Biyolojisi ve Terminolojisi dersinin 100 slaytlık tam kapsamlı interaktif öğrenme destesi.",
        "category": "Dönem 1 - Kurul 1",
        "department": "Tıbbi Patoloji",
        "lecturer": "Prof. Dr. Hikmet Keleş (Tıbbi Patoloji ABD)",
        "sourcePdf": "Kurul 1 - Ders 28: Tümör Biyolojisi ve Terminolojisi (Prof. Dr. Hikmet Keleş)",
        "slides": enriched_slides,
        "questions": questions,
        "flashcards": all_flashcards
    }

    # 6. RUNTIME ITEM OLUŞTUR
    os.makedirs(DECKS_ITEMS_DIR, exist_ok=True)
    runtime_item_path = os.path.join(DECKS_ITEMS_DIR, "k1p-k1-28-tumor-biyolojisi-ve-terminolojisi.json")
    with open(runtime_item_path, "w", encoding="utf-8") as f:
        json.dump(deck_data, f, ensure_ascii=False, indent=2)
    print(f"5. Runtime item yazıldı: {runtime_item_path}")

    # 7. MULTI-FORMAT PAKETLEME
    os.makedirs(PACKAGE_DIR, exist_ok=True)

    # 7a. manifest.json
    manifest = {
        "id": deck_data["id"],
        "title": deck_data["title"],
        "subtitle": deck_data["subtitle"],
        "slug": deck_data["slug"],
        "description": deck_data["description"],
        "department": deck_data["department"],
        "lecturer": deck_data["lecturer"],
        "sourcePdf": deck_data["sourcePdf"],
        "slideCount": len(enriched_slides),
        "questionCount": len(questions),
        "flashcardCount": len(all_flashcards),
        "elementCounts": dict(element_counts),
        "files": ["manifest.json", "content.md", "blocks.html", "structure.xml"]
    }
    with open(os.path.join(PACKAGE_DIR, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    # 7b. content.md
    with open(os.path.join(PACKAGE_DIR, "content.md"), "w", encoding="utf-8") as f:
        f.write(f"# {deck_data['title']}\n")
        f.write(f"## {deck_data['subtitle']}\n\n")
        f.write(f"**Eğitici:** {deck_data['lecturer']}\n")
        f.write(f"**Anabilim Dalı:** {deck_data['department']}\n")
        f.write(f"**Kaynak:** {deck_data['sourcePdf']}\n\n---\n\n")

        for s in enriched_slides:
            f.write(f"### Slayt {s['slideNumber']}: {s['title']}\n\n")
            f.write(f"{s['content']}\n\n")
            if s.get("flashcards"):
                f.write("#### Akıl Kartları (Flashcards)\n")
                for fc in s["flashcards"]:
                    f.write(f"- **Soru:** {fc['front']}\n  - **Cevap:** {fc['back']}\n  - *İpucu:* {fc['hint']}\n")
                f.write("\n")
            f.write("---\n\n")

    # 7c. blocks.html
    with open(os.path.join(PACKAGE_DIR, "blocks.html"), "w", encoding="utf-8") as f:
        f.write("<!DOCTYPE html>\n<html lang=\"tr\">\n<head>\n<meta charset=\"UTF-8\">\n")
        f.write(f"<title>{deck_data['title']}</title>\n")
        f.write("<style>body{font-family:sans-serif;margin:40px;line-height:1.6;} .slide{margin-bottom:40px;padding:20px;border:1px solid #ddd;border-radius:8px;} .fc{background:#f9f9f9;padding:10px;margin:5px 0;border-left:4px solid #3b82f6;}</style>\n</head>\n<body>\n")
        f.write(f"<h1>{deck_data['title']}</h1>\n<p><em>{deck_data['subtitle']}</em></p>\n")
        for s in enriched_slides:
            f.write(f"<div class=\"slide\" id=\"slide-{s['slideNumber']}\">\n")
            f.write(f"<h2>Slayt {s['slideNumber']}: {s['title']}</h2>\n")
            f.write(f"<p>{s['content']}</p>\n")
            if s.get("flashcards"):
                f.write("<h3>Akıl Kartları</h3>\n")
                for fc in s["flashcards"]:
                    f.write(f"<div class=\"fc\"><strong>S:</strong> {fc['front']}<br><strong>C:</strong> {fc['back']}</div>\n")
            f.write("</div>\n")
        f.write("</body>\n</html>\n")

    # 7d. structure.xml
    root = ET.Element("learningDeck", attrib={"id": deck_data["id"], "slideCount": str(len(enriched_slides))})
    meta = ET.SubElement(root, "metadata")
    ET.SubElement(meta, "title").text = deck_data["title"]
    ET.SubElement(meta, "subtitle").text = deck_data["subtitle"]
    ET.SubElement(meta, "lecturer").text = deck_data["lecturer"]
    ET.SubElement(meta, "department").text = deck_data["department"]

    slides_xml = ET.SubElement(root, "slides")
    for s in enriched_slides:
        s_el = ET.SubElement(slides_xml, "slide", attrib={"number": str(s["slideNumber"]), "id": s["id"]})
        ET.SubElement(s_el, "title").text = s["title"]
        ET.SubElement(s_el, "content").text = s["content"]
        if s.get("flashcards"):
            fcs_el = ET.SubElement(s_el, "flashcards")
            for fc in s["flashcards"]:
                fc_el = ET.SubElement(fcs_el, "flashcard", attrib={"id": fc["id"]})
                ET.SubElement(fc_el, "front").text = fc["front"]
                ET.SubElement(fc_el, "back").text = fc["back"]
                ET.SubElement(fc_el, "hint").text = fc["hint"]

    with open(os.path.join(PACKAGE_DIR, "structure.xml"), "w", encoding="utf-8") as f:
        f.write(prettify_xml(root))

    print(f"6. Multi-format paket üretildi: {PACKAGE_DIR}")

    # 8. YERİNDE GÜNCELLEME: interactive_learning_decks.json (İndeks 75)
    with open(INTERACTIVE_DECKS_PATH, "r", encoding="utf-8") as f:
        decks = json.load(f)

    target_idx = 75
    assert decks[target_idx]["id"] == deck_data["id"], f"HATA: İndeks {target_idx} hedef deste id'si ile uyuşmuyor: {decks[target_idx]['id']}"

    decks[target_idx]["slides"] = enriched_slides
    decks[target_idx]["questions"] = questions
    decks[target_idx]["flashcards"] = all_flashcards
    decks[target_idx]["slideCount"] = len(enriched_slides)
    decks[target_idx]["questionCount"] = len(questions)
    decks[target_idx]["flashcardCount"] = len(all_flashcards)
    decks[target_idx]["sourcePdf"] = deck_data["sourcePdf"]

    with open(INTERACTIVE_DECKS_PATH, "w", encoding="utf-8") as f:
        json.dump(decks, f, ensure_ascii=False, indent=2)
    print(f"7. {INTERACTIVE_DECKS_PATH} (indeks {target_idx}) yerinde güncellendi.")

    # 9. YERİNDE GÜNCELLEME: catalog.json (İndeks 75)
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    assert catalog[target_idx]["id"] == deck_data["id"], f"HATA: Katalog indeks {target_idx} id'si uyuşmuyor!"
    catalog[target_idx]["slideCount"] = len(enriched_slides)
    catalog[target_idx]["questionCount"] = len(questions)
    catalog[target_idx]["flashcardCount"] = len(all_flashcards)

    with open(CATALOG_PATH, "w", encoding="utf-8") as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2)
    print(f"8. {CATALOG_PATH} (indeks {target_idx}) yerinde güncellendi.")

    print("\n" + "=" * 60)
    print("DERS 28 BAŞARIYLA TAMAMLANDI VE PAKETLENDİ!")
    print("=" * 60)

if __name__ == "__main__":
    build_lesson_28_deck()
