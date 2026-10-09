# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 22: Bebek Beslenmesi
(Doç. Dr. Nergiz Sevinç - Halk Sağlığı ABD)
Master Deck Oluşturucu ve Multi-Format Paketleyici.

- 10 Bölüm, 100 Slayt, 10 Checkpoint
- 30 Akıl Kartı (Her checkpoint'te 3 adet, 0 hint leak)
- 7 İnteraktif Eleman Tipi (Her biri >= %8.0 çeşitlilik)
- Multi-format paketleme: manifest.json, content.md, blocks.html, structure.xml
- Runtime item: meds/src/data/decks/items/k1p-k1-22-bebek-beslenmesi.json
- Yerinde güncelleme: interactive_learning_decks.json (indeks 69) ve catalog.json
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

from scripts.k1_22_deck_data.section_1 import get_section_1_slides
from scripts.k1_22_deck_data.section_2 import get_section_2_slides
from scripts.k1_22_deck_data.section_3 import get_section_3_slides
from scripts.k1_22_deck_data.section_4 import get_section_4_slides
from scripts.k1_22_deck_data.section_5 import get_section_5_slides
from scripts.k1_22_deck_data.section_6 import get_section_6_slides
from scripts.k1_22_deck_data.section_7 import get_section_7_slides
from scripts.k1_22_deck_data.section_8 import get_section_8_slides
from scripts.k1_22_deck_data.section_9 import get_section_9_slides
from scripts.k1_22_deck_data.section_10 import get_section_10_slides
from scripts.enrich_k1_22_elements import apply_enrichment

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDS_DIR = os.path.join(BASE_DIR, "meds")
QUESTIONS_FILE = os.path.join(MEDS_DIR, "src/data/ornek_sorular/k1/k1-22-bebek-beslenmesi.json")
PACKAGE_DIR = os.path.join(MEDS_DIR, "src/data/decks/packages/k1p-k1-22-bebek-beslenmesi")
DECKS_ITEMS_DIR = os.path.join(MEDS_DIR, "src/data/decks/items")
INTERACTIVE_DECKS_PATH = os.path.join(MEDS_DIR, "src/data/interactive_learning_decks.json")
CATALOG_PATH = os.path.join(MEDS_DIR, "src/data/decks/catalog.json")

def leaks(hint, answer):
    if not hint or not answer:
        return False
    # Sayı kontrolü
    for d in re.findall(r"\b\d+\b", answer):
        if re.search(r"\b" + re.escape(d) + r"\b", hint):
            return True
    # Kelime kökü kontrolü
    stop_words = {"ve", "veya", "ile", "için", "olan", "bir", "bu", "şu", "da", "de", "ise", "en", "çok", "daha", "kadar"}
    ans_words = [w.lower() for w in re.findall(r"[a-zA-ZçğıöşüÇĞİÖŞÜ]+", answer) if len(w) >= 3 and w.lower() not in stop_words]
    for w in ans_words:
        stem = w[:4] if len(w) >= 4 else w
        if stem in hint.lower():
            return True
    return False

def build_lesson_22_deck():
    print("=" * 60)
    print("KURUL 1 - DERS 22: BEBEK BESLENMESİ")
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
            q_id = q.get("id") or f"k1-22-q{len(questions)+1:02d}"
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
        
        # Checkpoint akıl kartlarını ayır (hem slide['flashcards'] hem de elements içindeki flashcard'ları yakala)
        fcs = s.get("flashcards") or [el for el in raw_elements if isinstance(el, dict) and "front" in el]
        if fcs:
            checkpoint_cards_map[slide_num] = fcs
            
        clean_elements = [el for el in raw_elements if isinstance(el, dict) and el.get("type")]
        
        standardized_slides.append({
            "id": f"k1-22-s{slide_num:02d}",
            "slideNumber": slide_num,
            "title": title,
            "content": content,
            "sourcePdf": s.get("sourcePdf", "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları"),
            "elements": clean_elements
        })

    # apply_enrichment ile %8+ çeşitliliği sağla
    slides = apply_enrichment(standardized_slides)
    element_counts = Counter()
    for s in slides:
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
        s = slides[slide_idx]
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
        "id": "k1p-k1-22-bebek-beslenmesi",
        "title": "Bebek Beslenmesi",
        "subtitle": "Anne Sütü, Emzirme Dinamikleri, Tamamlayıcı Beslenme ve Çocukluk Çağı Malnütrisyonu",
        "slug": "k1p-k1-22-bebek-beslenmesi",
        "description": "Doç. Dr. Nergiz Sevinç (Halk Sağlığı ABD) tarafından hazırlanan Bebek Beslenmesi dersinin 100 slaytlık tam kapsamlı interaktif öğrenme destesi.",
        "category": "Dönem 1 - Kurul 1",
        "department": "Halk Sağlığı",
        "lecturer": "Doç. Dr. Nergiz Sevinç (Halk Sağlığı ABD)",
        "sourcePdf": "Kurul 1 - Ders 22: Bebek Beslenmesi (Doç. Dr. Nergiz Sevinç)",
        "slides": slides,
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
            "slideCount": len(slides),
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
    md_lines = [
        f"# {deck_data['title']}",
        f"**{deck_data['subtitle']}**\n",
        f"- **Öğretim Üyesi:** {deck_data['lecturer']}",
        f"- **Bölüm:** {deck_data['department']}",
        f"- **Kaynak:** {deck_data['sourcePdf']}\n",
        "## Slayt İçerikleri\n"
    ]
    for s in slides:
        md_lines.append(f"### Slayt {s['slideNumber']}: {s['title']}")
        md_lines.append(f"\n{s['content']}\n")
        if s.get("flashcards"):
            md_lines.append("#### Kontrol Noktası Akıl Kartları:")
            for fc in s["flashcards"]:
                md_lines.append(f"- **Soru:** {fc['front']}")
                md_lines.append(f"  - **Cevap:** {fc['back']}")
                md_lines.append(f"  - **İpucu:** {fc['hint']}")
            md_lines.append("")
        md_lines.append("---\n")

    with open(os.path.join(PACKAGE_DIR, "content.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    # 7c. blocks.html
    html_lines = [
        "<!DOCTYPE html>",
        "<html lang=\"tr\">",
        "<head>",
        "  <meta charset=\"UTF-8\">",
        f"  <title>{deck_data['title']}</title>",
        "  <style>",
        "    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; max-width: 900px; margin: 40px auto; padding: 0 20px; color: #1e293b; }",
        "    h1 { color: #0f172a; border-bottom: 2px solid #e2e8f0; padding-bottom: 12px; }",
        "    h2 { color: #1e40af; margin-top: 32px; }",
        "    .slide { border: 1px solid #e2e8f0; border-radius: 8px; padding: 20px; margin-bottom: 24px; background: #ffffff; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }",
        "    .checkpoint { border-left: 4px solid #3b82f6; background: #f8fafc; }",
        "    .card { background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 6px; padding: 12px; margin-top: 12px; }",
        "  </style>",
        "</head>",
        "<body>",
        f"  <h1>{deck_data['title']}</h1>",
        f"  <p><em>{deck_data['subtitle']}</em></p>",
        f"  <p><strong>Öğretim Üyesi:</strong> {deck_data['lecturer']} | <strong>Ders:</strong> {deck_data['department']}</p>"
    ]
    for s in slides:
        is_cp = bool(s.get("flashcards"))
        cp_cls = " slide checkpoint" if is_cp else " slide"
        html_lines.append(f"  <div class=\"{cp_cls}\">")
        html_lines.append(f"    <h2>Slayt {s['slideNumber']}: {s['title']}</h2>")
        html_lines.append(f"    <p>{s['content']}</p>")
        if is_cp:
            html_lines.append("    <h3>Kontrol Noktası Akıl Kartları:</h3>")
            for fc in s["flashcards"]:
                html_lines.append("    <div class=\"card\">")
                html_lines.append(f"      <p><strong>Soru:</strong> {fc['front']}</p>")
                html_lines.append(f"      <p><strong>Cevap:</strong> {fc['back']}</p>")
                html_lines.append(f"      <p><small><strong>İpucu:</strong> {fc['hint']}</small></p>")
                html_lines.append("    </div>")
        html_lines.append("  </div>")
    html_lines.append("</body>")
    html_lines.append("</html>")

    with open(os.path.join(PACKAGE_DIR, "blocks.html"), "w", encoding="utf-8") as f:
        f.write("\n".join(html_lines))

    # 7d. structure.xml
    root = ET.Element("deck", id=deck_data["id"])
    ET.SubElement(root, "title").text = deck_data["title"]
    ET.SubElement(root, "subtitle").text = deck_data["subtitle"]
    ET.SubElement(root, "department").text = deck_data["department"]
    ET.SubElement(root, "lecturer").text = deck_data["lecturer"]

    slides_node = ET.SubElement(root, "slides")
    for s in slides:
        s_node = ET.SubElement(slides_node, "slide", id=s["id"], number=str(s["slideNumber"]))
        ET.SubElement(s_node, "title").text = s["title"]
        ET.SubElement(s_node, "content").text = s["content"]
        if s.get("flashcards"):
            fcs_node = ET.SubElement(s_node, "flashcards")
            for fc in s["flashcards"]:
                fc_node = ET.SubElement(fcs_node, "flashcard", id=fc["id"])
                ET.SubElement(fc_node, "front").text = fc["front"]
                ET.SubElement(fc_node, "back").text = fc["back"]
                ET.SubElement(fc_node, "hint").text = fc.get("hint", "")

    xml_str = ET.tostring(root, encoding="utf-8")
    parsed_xml = minidom.parseString(xml_str)
    pretty_xml = parsed_xml.toprettyxml(indent="  ", encoding="utf-8").decode("utf-8")

    with open(os.path.join(PACKAGE_DIR, "structure.xml"), "w", encoding="utf-8") as f:
        f.write(pretty_xml)

    print(f"6. Multi-format paket dosyaları oluşturuldu: {PACKAGE_DIR}")

    # 8. INTERACTIVE_LEARNING_DECKS.JSON DOSYASINI YERİNDE GÜNCELLE (INDEX 69)
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
            "slideCount": len(slides),
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
    print("DERS 22 DECK BUILD VE PAKETLEME BAŞARIYLA TAMAMLANDI!")
    print("=" * 60)

if __name__ == "__main__":
    build_lesson_22_deck()
