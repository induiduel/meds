# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 27: Üriner Sistem Taş Hastalıkları Fizyopatolojisi
(Dr. Öğr. Üyesi Fahrettin Şamil Uysal - Üroloji ABD)
Master Deck Oluşturucu ve Multi-Format Paketleyici.

- 10 Bölüm, 100 Slayt, 10 Checkpoint
- 30 Akıl Kartı (Her checkpoint'te 3 adet, 0 hint leak)
- 7 İnteraktif Eleman Tipi (Her biri >= %8.0 çeşitlilik)
- Multi-format paketleme: manifest.json, content.md, blocks.html, structure.xml
- Runtime item: meds/src/data/decks/items/k1p-k1-27-uriner-sistem-tas-hastaliklari-fizyopatolojisi.json
- Yerinde güncelleme: interactive_learning_decks.json (indeks 74) ve catalog.json (indeks 74)
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

from scripts.k1_27_deck_data.section_1 import get_section_1_slides
from scripts.k1_27_deck_data.section_2 import get_section_2_slides
from scripts.k1_27_deck_data.section_3 import get_section_3_slides
from scripts.k1_27_deck_data.section_4 import get_section_4_slides
from scripts.k1_27_deck_data.section_5 import get_section_5_slides
from scripts.k1_27_deck_data.section_6 import get_section_6_slides
from scripts.k1_27_deck_data.section_7 import get_section_7_slides
from scripts.k1_27_deck_data.section_8 import get_section_8_slides
from scripts.k1_27_deck_data.section_9 import get_section_9_slides
from scripts.k1_27_deck_data.section_10 import get_section_10_slides
from scripts.enrich_k1_27_elements import enrich_slides

MEDS_DIR = os.path.join(BASE_DIR, "meds")
QUESTIONS_FILE = os.path.join(MEDS_DIR, "src/data/ornek_sorular/k1/k1-27-uriner-sistem-tas-hastaliklari-fizyopatolojisi.json")
PACKAGE_DIR = os.path.join(MEDS_DIR, "src/data/decks/packages/k1p-k1-27-uriner-sistem-tas-hastaliklari-fizyopatolojisi")
DECKS_ITEMS_DIR = os.path.join(MEDS_DIR, "src/data/decks/items")
INTERACTIVE_DECKS_PATH = os.path.join(MEDS_DIR, "src/data/interactive_learning_decks.json")
CATALOG_PATH = os.path.join(MEDS_DIR, "src/data/decks/catalog.json")

def normalize_text(text):
    text = text.lower()
    text = text.replace('i̇', 'i').replace('ı', 'i').replace('ş', 's').replace('ğ', 'g').replace('ü', 'u').replace('ö', 'o').replace('ç', 'c')
    return re.sub(r'[^a-z0-9]', ' ', text)

def leaks(hint, answer):
    if not hint or not answer:
        return False
    # Sayı kontrolü
    for d in re.findall(r"\b\d+\b", answer):
        if re.search(r"\b" + re.escape(d) + r"\b", hint):
            return True
    # Kelime ve 4 harfli kök kontrolü
    h_words = normalize_text(hint).split()
    a_words = normalize_text(answer).split()
    stop_words = {"ve", "veya", "ile", "icin", "olan", "bir", "bu", "su", "da", "de", "ise", "en", "cok", "daha", "kadar"}
    h_stems = {w[:4] for w in h_words if len(w) >= 4 and w not in stop_words}
    a_stems = {w[:4] for w in a_words if len(w) >= 4 and w not in stop_words}
    overlap = h_stems.intersection(a_stems)
    return len(overlap) > 0

def build_lesson_27_deck():
    print("=" * 60)
    print("KURUL 1 - DERS 27: ÜRİNER SİSTEM TAŞ HASTALIKLARI FİZYOPATOLOJİSİ")
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
            q_id = q.get("id") or f"k1-27-q{len(questions)+1:02d}"
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
            "id": f"k1-27-s{slide_num:02d}",
            "slideNumber": slide_num,
            "title": title,
            "content": content,
            "sourcePdf": s.get("sourcePdf", "Üroloji ABD - Üriner Sistem Taş Hastalıkları Fizyopatolojisi (Dr. Öğr. Üyesi Fahrettin Şamil Uysal)"),
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
        "id": "k1p-k1-27-uriner-sistem-tas-hastaliklari-fizyopatolojisi",
        "title": "Üriner Sistem Taş Hastalıkları Fizyopatolojisi",
        "subtitle": "Epidemiyoloji, Taş Sınıflaması, Fizikokimya ve Süpersatürasyon, İnhibitörler, Randall Plakları ve Kalsiyum/Non-Kalsiyum Litogenezi",
        "slug": "k1p-k1-27-uriner-sistem-tas-hastaliklari-fizyopatolojisi",
        "description": "Dr. Öğr. Üyesi Fahrettin Şamil Uysal (Üroloji ABD) tarafından hazırlanan Üriner Sistem Taş Hastalıkları Fizyopatolojisi dersinin 100 slaytlık tam kapsamlı interaktif öğrenme destesi.",
        "category": "Dönem 1 - Kurul 1",
        "department": "Üroloji",
        "lecturer": "Dr. Öğr. Üyesi Fahrettin Şamil Uysal (Üroloji ABD)",
        "sourcePdf": "Kurul 1 - Ders 27: Üriner Sistem Taş Hastalıkları Fizyopatolojisi (Dr. Öğr. Üyesi Fahrettin Şamil Uysal)",
        "slides": enriched_slides,
        "questions": questions,
        "flashcards": all_flashcards
    }

    # 6. RUNTIME ITEM OLUŞTUR
    os.makedirs(DECKS_ITEMS_DIR, exist_ok=True)
    item_path = os.path.join(DECKS_ITEMS_DIR, f"{deck_data['id']}.json")
    with open(item_path, "w", encoding="utf-8") as f:
        json.dump(deck_data, f, ensure_ascii=False, indent=2)
    print(f"5. Runtime item oluşturuldu: {item_path}")

    # 7. MULTI-FORMAT PAKET DOSYALARINI ÜRET
    os.makedirs(PACKAGE_DIR, exist_ok=True)

    # 7a. manifest.json
    manifest = {
        "id": deck_data["id"],
        "title": deck_data["title"],
        "subtitle": deck_data["subtitle"],
        "slug": deck_data["slug"],
        "version": "1.0.0",
        "category": deck_data["category"],
        "department": deck_data["department"],
        "lecturer": deck_data["lecturer"],
        "sourcePdf": deck_data["sourcePdf"],
        "stats": {
            "slideCount": len(enriched_slides),
            "questionCount": len(questions),
            "flashcardCount": len(all_flashcards),
            "elementCount": total_elements,
            "elementDiversity": {k: f"{v} (%{(v/total_elements)*100:.1f})" for k, v in element_counts.items()}
        },
        "files": {
            "structure": "structure.xml",
            "content": "content.md",
            "blocks": "blocks.html"
        }
    }
    with open(os.path.join(PACKAGE_DIR, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    # 7b. content.md
    with open(os.path.join(PACKAGE_DIR, "content.md"), "w", encoding="utf-8") as f:
        f.write(f"# {deck_data['title']}\n\n")
        f.write(f"**Alt Başlık:** {deck_data['subtitle']}\n")
        f.write(f"**Öğretim Üyesi:** {deck_data['lecturer']}\n")
        f.write(f"**Kaynak:** {deck_data['sourcePdf']}\n\n---\n\n")

        for s in enriched_slides:
            f.write(f"## Slayt {s['slideNumber']}: {s['title']}\n\n")
            f.write(f"{s['content']}\n\n")
            if s.get("flashcards"):
                f.write("### Akıl Kartları (Checkpoint Tekrarı)\n\n")
                for fc in s["flashcards"]:
                    f.write(f"- **Soru:** {fc['front']}\n")
                    f.write(f"  - **Cevap:** {fc['back']}\n")
                    f.write(f"  - *İpucu:* {fc['hint']}\n\n")
            if s.get("elements"):
                f.write(f"*İnteraktif Elemanlar ({len(s['elements'])} adet)*\n\n")
                for el in s["elements"]:
                    f.write(f"- `{el.get('type')}`: {el.get('title') or el.get('question') or el.get('scenario') or el.get('sentence', '')[:60]}...\n")
            f.write("\n---\n\n")

    # 7c. blocks.html
    with open(os.path.join(PACKAGE_DIR, "blocks.html"), "w", encoding="utf-8") as f:
        f.write("<!DOCTYPE html>\n<html lang=\"tr\">\n<head>\n")
        f.write("  <meta charset=\"UTF-8\">\n")
        f.write(f"  <title>{deck_data['title']}</title>\n")
        f.write("  <style>\n")
        f.write("    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; max-width: 900px; margin: 0 auto; padding: 20px; color: #1e293b; background: #f8fafc; }\n")
        f.write("    .slide-card { background: white; border-radius: 12px; padding: 24px; margin-bottom: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); border-left: 5px solid #0284c7; }\n")
        f.write("    .checkpoint { border-left-color: #10b981; background: #f0fdf4; }\n")
        f.write("    h1 { color: #0f172a; text-align: center; }\n")
        f.write("    h2 { color: #0369a1; margin-top: 0; }\n")
        f.write("    .meta { font-size: 0.9em; color: #64748b; margin-bottom: 12px; }\n")
        f.write("    .flashcard { background: #f1f5f9; padding: 12px 16px; border-radius: 8px; margin: 8px 0; border-left: 3px solid #6366f1; }\n")
        f.write("    .element-pill { display: inline-block; background: #e0f2fe; color: #0369a1; padding: 4px 10px; border-radius: 16px; font-size: 0.8em; margin: 4px 2px; font-weight: 500; }\n")
        f.write("  </style>\n</head>\n<body>\n")
        f.write(f"  <h1>{deck_data['title']}</h1>\n")
        f.write(f"  <p style=\"text-align:center; color:#64748b;\">{deck_data['subtitle']}</p>\n\n")

        for s in enriched_slides:
            is_cp = "[TEKRAR SAYFASI" in s["title"]
            f.write(f"  <div class=\"slide-card {'checkpoint' if is_cp else ''}\">\n")
            f.write(f"    <div class=\"meta\">Slayt #{s['slideNumber']} · {s.get('sourcePdf', '')}</div>\n")
            f.write(f"    <h2>{s['title']}</h2>\n")
            f.write(f"    <p>{s['content']}</p>\n")

            if s.get("flashcards"):
                f.write("    <div style=\"margin-top:16px;\"><strong>Akıl Kartları:</strong>\n")
                for fc in s["flashcards"]:
                    f.write(f"      <div class=\"flashcard\"><strong>S:</strong> {fc['front']}<br><strong>C:</strong> {fc['back']}</div>\n")
                f.write("    </div>\n")

            if s.get("elements"):
                f.write("    <div style=\"margin-top:12px;\">\n")
                for el in s["elements"]:
                    f.write(f"      <span class=\"element-pill\">{el.get('type')}</span>\n")
                f.write("    </div>\n")
            f.write("  </div>\n\n")

        f.write("</body>\n</html>\n")

    # 7d. structure.xml
    root = ET.Element("learningDeck", attrib={"id": deck_data["id"], "version": "1.0"})
    meta = ET.SubElement(root, "metadata")
    ET.SubElement(meta, "title").text = deck_data["title"]
    ET.SubElement(meta, "subtitle").text = deck_data["subtitle"]
    ET.SubElement(meta, "lecturer").text = deck_data["lecturer"]
    ET.SubElement(meta, "slideCount").text = str(len(enriched_slides))
    ET.SubElement(meta, "questionCount").text = str(len(questions))
    ET.SubElement(meta, "flashcardCount").text = str(len(all_flashcards))

    slides_xml = ET.SubElement(root, "slides")
    for s in enriched_slides:
        s_el = ET.SubElement(slides_xml, "slide", attrib={"number": str(s["slideNumber"]), "id": s["id"]})
        ET.SubElement(s_el, "title").text = s["title"]
        ET.SubElement(s_el, "content").text = s["content"]
        if s.get("flashcards"):
            fc_el = ET.SubElement(s_el, "flashcards")
            for fc in s["flashcards"]:
                card_el = ET.SubElement(fc_el, "card", attrib={"id": fc["id"]})
                ET.SubElement(card_el, "front").text = fc["front"]
                ET.SubElement(card_el, "back").text = fc["back"]
                ET.SubElement(card_el, "hint").text = fc.get("hint", "")

        if s.get("elements"):
            elems_el = ET.SubElement(s_el, "interactiveElements")
            for el in s["elements"]:
                ET.SubElement(elems_el, "element", attrib={"type": el.get("type", "")})

    xml_str = ET.tostring(root, encoding="utf-8")
    pretty_xml = minidom.parseString(xml_str).toprettyxml(indent="  ")
    with open(os.path.join(PACKAGE_DIR, "structure.xml"), "w", encoding="utf-8") as f:
        f.write(pretty_xml)

    print(f"6. Multi-format paket dosyaları başarıyla üretildi: {PACKAGE_DIR}")

    # 8. INTERACTIVE_LEARNING_DECKS.JSON DOSYASINI YERİNDE GÜNCELLE
    if os.path.exists(INTERACTIVE_DECKS_PATH):
        with open(INTERACTIVE_DECKS_PATH, "r", encoding="utf-8") as f:
            decks_list = json.load(f)

        target_idx = None
        for i, d in enumerate(decks_list):
            if d.get("id") == deck_data["id"]:
                target_idx = i
                break

        if target_idx is not None:
            decks_list[target_idx] = deck_data
            print(f"7. interactive_learning_decks.json içinde indeks {target_idx} yerinde güncellendi.")
        else:
            decks_list.append(deck_data)
            print("7. interactive_learning_decks.json sonuna yeni deste olarak eklendi.")

        with open(INTERACTIVE_DECKS_PATH, "w", encoding="utf-8") as f:
            json.dump(decks_list, f, ensure_ascii=False, indent=2)

    # 9. CATALOG.JSON DOSYASINI GÜNCELLE
    if os.path.exists(CATALOG_PATH):
        with open(CATALOG_PATH, "r", encoding="utf-8") as f:
            catalog_list = json.load(f)

        cat_target = None
        for i, c in enumerate(catalog_list):
            if c.get("id") == deck_data["id"]:
                cat_target = i
                break

        cat_entry = {
            "id": deck_data["id"],
            "title": deck_data["title"],
            "subtitle": deck_data["subtitle"],
            "category": deck_data["category"],
            "department": deck_data["department"],
            "lecturer": deck_data["lecturer"],
            "slideCount": len(enriched_slides),
            "questionCount": len(questions),
            "flashcardCount": len(all_flashcards),
            "sourcePdf": deck_data["sourcePdf"]
        }

        if cat_target is not None:
            catalog_list[cat_target] = cat_entry
            print(f"8. catalog.json içinde indeks {cat_target} güncellendi.")
        else:
            catalog_list.append(cat_entry)
            print("8. catalog.json listesine eklendi.")

        with open(CATALOG_PATH, "w", encoding="utf-8") as f:
            json.dump(catalog_list, f, ensure_ascii=False, indent=2)

    print("=" * 60)
    print("DERS 27 DECK BUILD VE PAKETLEME BAŞARIYLA TAMAMLANDI!")
    print("=" * 60)

if __name__ == "__main__":
    build_lesson_27_deck()
