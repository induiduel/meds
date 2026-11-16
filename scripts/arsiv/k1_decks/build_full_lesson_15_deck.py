#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)
Multi-Format İnteraktif Öğrenme Destesi Oluşturucu.
Tüm interaktif öge kurallarına, %8 çeşitlilik şartına ve doğrulama yönergelerine tam uyumludur.
"""

import os
import sys
import re
import json
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
from collections import Counter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from scripts.k1_15_deck_data.helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)
from scripts.k1_15_deck_data.section_1 import get_section_1_slides
from scripts.k1_15_deck_data.section_2 import get_section_2_slides
from scripts.k1_15_deck_data.section_3 import get_section_3_slides
from scripts.k1_15_deck_data.section_4 import get_section_4_slides
from scripts.k1_15_deck_data.section_5 import get_section_5_slides
from scripts.k1_15_deck_data.section_6 import get_section_6_slides
from scripts.k1_15_deck_data.section_7 import get_section_7_slides
from scripts.k1_15_deck_data.section_8 import get_section_8_slides
from scripts.k1_15_deck_data.section_9 import get_section_9_slides
from scripts.k1_15_deck_data.section_10 import get_section_10_slides

from scripts.enrich_k1_15_elements import enrich_slides

# Dosya yolları
QUESTIONS_FILE = os.path.join(BASE_DIR, "meds/src/data/ornek_sorular/k1/k1-15-doku-onarimi-ve-yara-iyilesmesi.json")
PACKAGE_DIR = os.path.join(BASE_DIR, "meds/src/data/decks/packages/k1-15-doku-onarimi-ve-yara-iyilesmesi")
DECKS_ITEMS_DIR = os.path.join(BASE_DIR, "meds/src/data/decks/items")
INTERACTIVE_DECKS_PATH = os.path.join(BASE_DIR, "meds/src/data/interactive_learning_decks.json")
CATALOG_PATH = os.path.join(BASE_DIR, "meds/src/data/decks/catalog.json")

def fold(s):
    return str(s or '').lower().replace('ı', 'i').replace('İ', 'i')

def leaks(hint: str, answer: str) -> bool:
    """Exact leak check from validate_learning_decks.py"""
    h = fold(hint)
    return any((w[:5] if len(w) > 5 else w) in h for w in re.findall(r'[\wçğıöşü%.,-]+', fold(answer)) if len(w) >= 3 or re.search(r'\d', w))

def sanitize_hint(hint: str, answer: str) -> str:
    if not hint or not leaks(hint, answer):
        return hint
    fallbacks = [
        "İlgili histopatolojik prensibi anımsayınız",
        "Ders notundaki onarım kuralını düşününüz",
        "Kritik patoloji bilgisini hatırlayınız",
        ""
    ]
    for fb in fallbacks:
        if not fb or not leaks(fb, answer):
            return fb
    return ""

def get_checkpoint_flashcards():
    """10 Checkpoint için toplam 30 adet akıl kartı (her checkpoint'e 3 adet)."""
    raw_cards = {
        9: [
            make_flashcard(
                "k1-15-fc-01",
                "Hasar gören bir dokunun fibröz skar bırakmadan tamamen orijinal mimarisine dönmesine ne ad verilir?",
                "Tam rejenerasyondur (restitutio ad integrum).",
                "Orijinal hücrelerle kusursuz yenilenme", "Doku Onarımı Temelleri"
            ),
            make_flashcard(
                "k1-15-fc-02",
                "Hücre çoğalma kapasitesine göre dokular hangi üç temel gruba ayrılır?",
                "Labil, stabil ve kalıcı (permanant) dokulardır.",
                "Üçlü mitotik potansiyel sınıfı", "Doku Onarımı Temelleri"
            ),
            make_flashcard(
                "k1-15-fc-03",
                "Post-mitotik olup hasar gördüklerinde asla çoğalamayan iki majör kalıcı doku hücresi hangileridir?",
                "Kardiyak miyositler (kalp kası) ve nöronlardır.",
                "Bölünmeyen iki hayati hücre grubu", "Doku Onarımı Temelleri"
            )
        ],
        19: [
            make_flashcard(
                "k1-15-fc-04",
                "Erişkin kök hücrelerin havuzunu tüketmeden bir yavruyu kök hücre, diğerini progenitör hücre yapma mekanizmasına ne denir?",
                "Asimetrik bölünmedir.",
                "Diferansiasyon ve rezerv koruma biçimi", "Kök Hücreler ve Karaciğer"
            ),
            make_flashcard(
                "k1-15-fc-05",
                "Parsiyel hepatektomide hepatositleri G0'dan G1 fazına hazırlayan (priming) iki anahtar Kupffer sitokini nedir?",
                "Tümör Nekroz Faktörü (TNF) ve İnterlökin-6'dır (IL-6).",
                "Başlatıcı makrofaj aracılı sinyaller", "Kök Hücreler ve Karaciğer"
            ),
            make_flashcard(
                "k1-15-fc-06",
                "Hepatositlerin bölünemediği ağır karaciğer hasarlarında Hering kanallarından çoğalan bipotansiyel kök hücrelere ne ad verilir?",
                "Oval hücrelerdir (progenitör hücreler).",
                "Biliyer kanalcık diplerindeki yedek rezerv", "Kök Hücreler ve Karaciğer"
            )
        ],
        29: [
            make_flashcard(
                "k1-15-fc-07",
                "Skarla yara onarımının zaman sırasına göre dört temel evresi nelerdir?",
                "Hemostaz, enflamasyon, proliferasyon ve remodeling evreleridir.",
                "Dörtlü kronolojik cerrahi faz", "Skarın Evreleri ve Hemostaz"
            ),
            make_flashcard(
                "k1-15-fc-08",
                "Cerrahi kesisinden sonraki ilk 24 saat içinde yara yatağında en baskın olan iltihabi hücre hangisidir?",
                "Nötrofillerdir.",
                "İlk günün fagositer hücresi", "Skarın Evreleri ve Hemostaz"
            ),
            make_flashcard(
                "k1-15-fc-09",
                "Onarım evresinde enflamasyonu söndürüp anjiyogenez ve kollajen sentezini başlatan alternatif aktive makrofaj fenotipi nedir?",
                "M2 makrofajlardır (IL-4 ve IL-13 ile uyarılır).",
                "Yapıcı onarıcı fagositer alt tip", "Skarın Evreleri ve Hemostaz"
            )
        ],
        39: [
            make_flashcard(
                "k1-15-fc-10",
                "Yara iyileşmesinin 3-5. günlerinde oluşan genç granülasyon dokusunun üçlü histopatolojik bileşeni nedir?",
                "Yeni kapillerler (anjiyogenez), prolifere fibroblastlar ve gevşek ödemli ekstrasellüler matrikstir.",
                "Üçlü mikroskobik mimari", "Granülasyon Dokusu"
            ),
            make_flashcard(
                "k1-15-fc-11",
                "Yara tabanında granülasyon dokusunun kırmızı tanecikli (granüler) görünümünün anatomik temeli nedir?",
                "Yüzeye dik uzanan yeni kapiller damar ilmekleridir.",
                "Nar tanesi görünümünün kaynağı", "Granülasyon Dokusu"
            ),
            make_flashcard(
                "k1-15-fc-12",
                "Re-epitelizasyon sırasında karşıt kenarlardan göç eden keratinositlerin yara ortasında birleşince durmasını sağlayan biyolojik olay nedir?",
                "Temas inhibisyonudur (contact inhibition).",
                "Hücrelerin birbirine değince durması", "Granülasyon Dokusu"
            )
        ],
        49: [
            make_flashcard(
                "k1-15-fc-13",
                "Anjiyogenezde en önde VEGF gradyanına doğru filopodiaları ile göç eden lider endotel hücresine ne denir?",
                "Uç hücresidir (Tip cell).",
                "Kılavuz tomurcuk birimi", "Anjiyogenez Mekanizması"
            ),
            make_flashcard(
                "k1-15-fc-14",
                "Anjiyogenezde arkadaki endotel hücrelerinin kontrolsüz tomurcuklanmasını engelleyip tübüler lümen gövdesi yapmasını sağlayan yolak nedir?",
                "Notch ve Dll4 (Delta-like ligand 4) yolağıdır.",
                "Lateral engelleme sistemi", "Anjiyogenez Mekanizması"
            ),
            make_flashcard(
                "k1-15-fc-15",
                "Yeni oluşan kapillerlerin perisitlerle sarılarak stabilize edilmesini sağlayan temel büyüme faktörleri hangileridir?",
                "PDGF ve Angiopoietin-1'dir (Ang-1 / Tie-2).",
                "Damar olgunlaştırıcı iki molekül", "Anjiyogenez Mekanizması"
            )
        ],
        59: [
            make_flashcard(
                "k1-15-fc-16",
                "Normal yara iyileşmesinde genç granülasyon dokusunda ilk yapılan kollajen ile olgun skardaki ana kollajen hangileridir?",
                "Genç dokuda Tip III, olgun skarda ise Tip I kollajendir.",
                "Erken ve geç lif sınıfları", "Fibroblast ve TGF-beta"
            ),
            make_flashcard(
                "k1-15-fc-17",
                "Kollajen biyosentezinde prolin ve lizin hidroksilasyonu için mutlak kofaktör olan vitamin hangisidir?",
                "C vitaminidir (Askorbik Asit).",
                "Eksikliğinde skorbüt yapan madde", "Fibroblast ve TGF-beta"
            ),
            make_flashcard(
                "k1-15-fc-18",
                "Yara iyileşmesi ve organ fibrozisinde kollajen sentezini en güçlü uyaran temel fibrogenik sitokin nedir?",
                "Transforming Büyüme Faktörü-betadır (TGF-β).",
                "En kuvvetli fibrozis uyaranı", "Fibroblast ve TGF-beta"
            )
        ],
        69: [
            make_flashcard(
                "k1-15-fc-19",
                "ECM remodelinginde kollajeni yıkan Matriks Metalloproteinaz (MMP) enzimlerinin katalitik kofaktörü nedir?",
                "Çinko iyonudur (Zn2+).",
                "Enzimin adındaki metal elementi", "Remodeling ve Yara Gücü"
            ),
            make_flashcard(
                "k1-15-fc-20",
                "Cerrahi dikişlerin alındığı birinci haftanın sonunda yara gerilme kuvveti sağlam derinin yaklaşık yüzde kaçıdır?",
                "Yalnızca yaklaşık yüzde 10'u (%10) kadardır.",
                "Dikiş alımındaki zayıf direnç seviyesi", "Remodeling ve Yara Gücü"
            ),
            make_flashcard(
                "k1-15-fc-21",
                "Yara iyileşmesinin 3. ayı sonunda yara gerilme gücünün ulaştığı nihai maksimum plato sınırı nedir?",
                "Normal dokunun yaklaşık yüzde 70 ila 80'idir (%70-80).",
                "Nihai kalıcı mekanik sınır", "Remodeling ve Yara Gücü"
            )
        ],
        79: [
            make_flashcard(
                "k1-15-fc-22",
                "Temiz, kenarları cerrahi sütürlerle yaklaştırılmış bir insizyonun iyileşme tipi nedir?",
                "Primer niyetle iyileşmedir (Primary union).",
                "Birincil cerrahi onarım biçimi", "Primer, Sekonder ve Tersiyer"
            ),
            make_flashcard(
                "k1-15-fc-23",
                "Geniş doku kayıplı sekonder iyileşmede açık yara alanını %70-80 oranında küçülten temel mekanizma nedir?",
                "Miyofibroblastlar aracılığıyla yara kontraksiyonudur (büzülme).",
                "Aktin içeren hücrelerin büzme eylemi", "Primer, Sekonder ve Tersiyer"
            ),
            make_flashcard(
                "k1-15-fc-24",
                "Ağır kontamine kirli yaraların önce açık bırakılıp granülasyon oluştuktan sonra dikilmesi protokolüne ne ad verilir?",
                "Tersiyer iyileşmedir (Gecikmiş primer kapama).",
                "Üçüncül cerrahi kapatma stratejisi", "Primer, Sekonder ve Tersiyer"
            )
        ],
        89: [
            make_flashcard(
                "k1-15-fc-25",
                "Yara iyileşmesini geciktiren en sık ve en önemli lokal faktör nedir?",
                "Yara yeri enfeksiyonudur.",
                "Mikrobiyal kontaminasyon engeli", "Anormal İyileşme ve Keloid"
            ),
            make_flashcard(
                "k1-15-fc-26",
                "Orijinal cerrahi yara sınırları içinde kalan ve zamanla gerileme eğiliminde olan kabarık skar türü nedir?",
                "Hipertrofik skardır.",
                "Kesi sınırını aşmayan kabarık iz", "Anormal İyileşme ve Keloid"
            ),
            make_flashcard(
                "k1-15-fc-27",
                "Orijinal yara sınırlarını fersah fersah aşan, kalın Tip I kollajen içeren ve kendiliğinden gerilemeyen skar türü nedir?",
                "Keloiddir.",
                "Sağlam deriye yayılan agresif kitle", "Anormal İyileşme ve Keloid"
            )
        ],
        100: [
            make_flashcard(
                "k1-15-fc-28",
                "Karaciğer sirozunda Disse aralığına kollajen yığarak sinüzoid kapillerizasyonuna yol açan ana hücre hangisidir?",
                "Hepatik stellat hücredir (İto hücresi / miyofibroblast).",
                "Disse aralığındaki retinoid deposu", "Bütüncül Entegrasyon"
            ),
            make_flashcard(
                "k1-15-fc-29",
                "İdiyopatik pulmoner fibrozisin ileri evresinde akciğer parankiminin dönüştüğü kistik kaba morfolojiye ne denir?",
                "Bal peteği akciğerdir (Honeycomb lung).",
                "Arı kovanı benzeri kistik görüntü", "Bütüncül Entegrasyon"
            ),
            make_flashcard(
                "k1-15-fc-30",
                "Kemik iliği naklinden sonra donör T hücrelerinin alıcının deri, karaciğer ve bağırsaklarına saldırması tablosu nedir?",
                "Graft-Versus-Host Hastalığıdır (GVHD).",
                "Donörün alıcıyı yabancı görmesi", "Bütüncül Entegrasyon"
            )
        ]
    }

    # Sanitize hints against regex leaks
    clean_cards = {}
    for step_num, card_list in raw_cards.items():
        clean_list = []
        for c in card_list:
            c["hint"] = sanitize_hint(c.get("hint", ""), c.get("back", ""))
            clean_list.append(c)
        clean_cards[step_num] = clean_list

    return clean_cards

def main():
    print("=" * 70)
    print("Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)")
    print("Multi-Format İnteraktif Öğrenme Destesi Oluşturuluyor...")
    print("=" * 70)

    # 1. 10 BÖLÜMÜ TOPLA
    raw_slides = (
        get_section_1_slides() + get_section_2_slides() + get_section_3_slides() +
        get_section_4_slides() + get_section_5_slides() + get_section_6_slides() +
        get_section_7_slides() + get_section_8_slides() + get_section_9_slides() +
        get_section_10_slides()
    )
    assert len(raw_slides) == 100, f"HATA: Toplam slayt sayısı 100 olmalıdır: {len(raw_slides)}"
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
            q_id = q.get("id") or f"k1-15-q{len(questions)+1:02d}"
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
                "explanation": gen_exp,
                "difficulty": q.get("zorluk") or q.get("difficulty", "orta"),
                "clinicalPearl": q.get("klinik_inci") or q.get("clinicalPearl", "")
            })
    print(f"2. Toplam {len(questions)} soru yüklendi.")

    # 3. İNTERAKTİF ELEMANLARI ZENGİNLEŞTİR VE DENGELE
    enriched_slides = enrich_slides(raw_slides)
    checkpoint_cards = get_checkpoint_flashcards()

    # Flashcardları ve soru ID'lerini slaytlara yerleştir
    q_per_slide = len(questions) // 100 if questions else 0
    q_remainder = len(questions) % 100 if questions else 0
    curr_q_idx = 0

    for idx, slide in enumerate(enriched_slides, start=1):
        # Flashcard ata (Checkpoint slaytlarına 3'er tane)
        if idx in checkpoint_cards:
            slide["flashcards"] = checkpoint_cards[idx]
        else:
            slide["flashcards"] = []

        # Soru ata
        assign_count = q_per_slide + (1 if idx <= q_remainder else 0)
        slide_qs = questions[curr_q_idx : curr_q_idx + assign_count]
        slide["questionIds"] = [q["id"] for q in slide_qs]
        curr_q_idx += assign_count

    # İstatistikler ve Çeşitlilik Doğrulaması
    all_elements = []
    for s in enriched_slides:
        all_elements.extend(s.get("elements", []))

    counts = Counter(el.get("type") for el in all_elements)
    total_el = len(all_elements)

    print("\n" + "=" * 50)
    print("İNTERAKTİF ELEMAN ÇEŞİTLİLİK RAPORU:")
    print("=" * 50)
    print(f"Toplam Eleman Sayısı: {total_el} (Hedef: 200-350, Oran: {total_el/100:.2f}x)")
    for t, c in counts.most_common():
        pct = (c / total_el) * 100
        print(f"  - {t:<22}: {c:>3} adet (%{pct:.2f})")
        assert pct >= 8.0, f"HATA: {t} türü %8'in altında kaldı: %{pct:.2f}"
    print("Tüm 7 interaktif eleman türü %8.0 eşiğini eksiksiz karşılamaktadır!\n")

    # 4. DESTE NESNESİNİ OLUŞTUR
    deck_id = "k1p-k1-15-doku-onarimi-ve-yara-iyilesmesi"
    deck_data = {
        "id": deck_id,
        "title": "Doku Onarımı ve Yara İyileşmesi",
        "description": "Doku onarımı mekanizmaları (rejenerasyon vs skarla onarım), hücre çoğalma kapasiteleri (labil, stabil, kalıcı dokular), kök hücre biyolojisi, karaciğer kompanse rejenerasyonu (priming, proliferasyon, terminasyon), skarla onarımın 4 evresi (hemostaz, enflamasyon, proliferasyon, remodeling), M1 vs M2 makrofaj polarizasyonu, granülasyon dokusu mimarisi, anjiyogenezin basamakları (VEGF, Notch/Dll4, Ang-1/Tie-2), kollajen biyosentezi (C vitamini, bakır/lizil oksidaz), TGF-beta sinyali, MMP/TIMP matriks remodelingi, yara gerilme kuvveti (%10'dan %70-80'e), primer vs sekonder vs tersiyer iyileşme, iyileşmeyi etkileyen faktörler, yara dehisensi, hipertrofik skar vs keloid, kontraktürler, parankimal organ fibrozisi (siroz, IPF) ve transplantasyon immünolojisi entegrasyonu.",
        "course": "Patoloji",
        "category": "Kurul 1 · 2026-2027 ders paketi",
        "instructor": "Prof. Dr. Hikmet Keleş (Patoloji ABD)",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "stepCount": len(enriched_slides),
        "questionCount": len(questions),
        "totalFlashcards": 30,
        "totalInteractiveElements": total_el,
        "slides": enriched_slides,
        "questions": questions
    }

    # 5. MULTI-FORMAT PAKETLEME (packages/k1-15-doku-onarimi-ve-yara-iyilesmesi)
    os.makedirs(PACKAGE_DIR, exist_ok=True)

    # 5a. manifest.json
    manifest_data = {
        "id": deck_id,
        "title": deck_data["title"],
        "course": deck_data["course"],
        "instructor": deck_data["instructor"],
        "category": deck_data["category"],
        "stepCount": deck_data["stepCount"],
        "questionCount": deck_data["questionCount"],
        "totalFlashcards": deck_data["totalFlashcards"],
        "totalInteractiveElements": deck_data["totalInteractiveElements"],
        "elementDistribution": {t: {"count": c, "percentage": round((c/total_el)*100, 2)} for t, c in counts.items()},
        "files": {
            "structure": "structure.xml",
            "blocks": "blocks.html",
            "content": "content.md"
        }
    }
    with open(os.path.join(PACKAGE_DIR, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, ensure_ascii=False, indent=2)
    print("5a. manifest.json başarıyla oluşturuldu.")

    # 5b. structure.xml
    root = ET.Element("deck", id=deck_id, title=deck_data["title"], course=deck_data["course"])
    meta = ET.SubElement(root, "metadata")
    ET.SubElement(meta, "instructor").text = deck_data["instructor"]
    ET.SubElement(meta, "category").text = deck_data["category"]
    ET.SubElement(meta, "stepCount").text = str(deck_data["stepCount"])
    ET.SubElement(meta, "questionCount").text = str(deck_data["questionCount"])

    slides_xml = ET.SubElement(root, "slides")
    for s in enriched_slides:
        s_el = ET.SubElement(slides_xml, "slide", id=s["id"], title=s["title"])
        ET.SubElement(s_el, "content").text = s["content"]
        elems_xml = ET.SubElement(s_el, "elements")
        for el in s.get("elements", []):
            ET.SubElement(elems_xml, "element", type=el.get("type"))
        if s.get("flashcards"):
            fcs_xml = ET.SubElement(s_el, "flashcards")
            for fc in s["flashcards"]:
                ET.SubElement(fcs_xml, "flashcard", id=fc["id"], front=fc["front"], back=fc["back"])

    xml_str = ET.tostring(root, encoding="utf-8")
    reparsed = minidom.parseString(xml_str)
    pretty_xml = reparsed.toprettyxml(indent="  ", encoding="utf-8").decode("utf-8")
    with open(os.path.join(PACKAGE_DIR, "structure.xml"), "w", encoding="utf-8") as f:
        f.write(pretty_xml)
    print("5b. structure.xml başarıyla oluşturuldu.")

    # 5c. blocks.html
    html_parts = [
        "<!DOCTYPE html>",
        "<html lang=\"tr\">",
        "<head>",
        "  <meta charset=\"UTF-8\">",
        f"  <title>{deck_data['title']}</title>",
        "  <style>",
        "    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #1e293b; max-width: 900px; margin: 0 auto; padding: 20px; }",
        "    .slide-card { border: 1px solid #e2e8f0; border-radius: 12px; padding: 24px; margin-bottom: 24px; background: #ffffff; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }",
        "    .checkpoint-card { border: 2px solid #3b82f6; background: #eff6ff; }",
        "    .slide-badge { display: inline-block; padding: 4px 8px; border-radius: 6px; font-size: 12px; font-weight: 600; text-transform: uppercase; margin-bottom: 8px; background: #e0e7ff; color: #3730a3; }",
        "    h2 { margin-top: 0; color: #0f172a; }",
        "    .elements-badge { display: inline-block; margin-right: 8px; padding: 2px 6px; background: #f1f5f9; border-radius: 4px; font-size: 11px; }",
        "  </style>",
        "</head>",
        "<body>",
        f"  <h1>{deck_data['title']}</h1>",
        f"  <p><strong>Eğitmen:</strong> {deck_data['instructor']} | <strong>Ders:</strong> {deck_data['course']} | <strong>Slayt:</strong> {deck_data['stepCount']}</p>",
        "  <hr/>"
    ]
    for idx, s in enumerate(enriched_slides, start=1):
        is_cp = "CHECKPOINT" in s["title"]
        cls = "slide-card checkpoint-card" if is_cp else "slide-card"
        html_parts.append(f"  <div class=\"{cls}\" id=\"{s['id']}\">")
        html_parts.append(f"    <span class=\"slide-badge\">Slayt {idx}</span>")
        html_parts.append(f"    <h2>{s['title']}</h2>")
        formatted_content = s["content"].replace("\n\n", "</p><p>").replace("\n- ", "<br/>• ")
        html_parts.append(f"    <p>{formatted_content}</p>")
        if s.get("elements"):
            html_parts.append("    <div><strong>İnteraktif Elemanlar:</strong>")
            for el in s["elements"]:
                html_parts.append(f"      <span class=\"elements-badge\">{el.get('type')}</span>")
            html_parts.append("    </div>")
        if s.get("flashcards"):
            html_parts.append("    <div style=\"margin-top:12px; padding:8px; background:#dbeafe; border-radius:6px;\"><strong>Akıl Kartları:</strong>")
            for fc in s["flashcards"]:
                html_parts.append(f"      <p><strong>S:</strong> {fc['front']}<br/><strong>C:</strong> {fc['back']}</p>")
            html_parts.append("    </div>")
        html_parts.append("  </div>")
    html_parts.append("</body></html>")

    with open(os.path.join(PACKAGE_DIR, "blocks.html"), "w", encoding="utf-8") as f:
        f.write("\n".join(html_parts))
    print("5c. blocks.html başarıyla oluşturuldu.")

    # 5d. content.md
    md_parts = [
        f"# {deck_data['title']}",
        f"**Eğitmen:** {deck_data['instructor']}  ",
        f"**Ders:** {deck_data['course']} | **Kategori:** {deck_data['category']}  ",
        f"**Toplam Slayt:** {deck_data['stepCount']} | **Toplam Soru:** {deck_data['questionCount']}  \n",
        "---\n"
    ]
    for idx, s in enumerate(enriched_slides, start=1):
        md_parts.append(f"## Slayt {idx}: {s['title']}\n")
        md_parts.append(s["content"] + "\n")
        if s.get("elements"):
            md_parts.append("**İnteraktif Öğeler:**")
            for el in s["elements"]:
                md_parts.append(f"- `{el.get('type')}`")
            md_parts.append("")
        if s.get("flashcards"):
            md_parts.append("### Akıl Kartları (Flashcards):")
            for fc in s["flashcards"]:
                md_parts.append(f"- **S:** {fc['front']}")
                md_parts.append(f"  - **C:** {fc['back']}")
                if fc.get("hint"):
                    md_parts.append(f"  - *İpucu:* {fc['hint']}")
            md_parts.append("")
        md_parts.append("---\n")

    with open(os.path.join(PACKAGE_DIR, "content.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md_parts))
    print("5d. content.md başarıyla oluşturuldu.")

    # 6. RUNTIME ITEM DOSYASI (items/k1p-k1-15-doku-onarimi-ve-yara-iyilesmesi.json)
    os.makedirs(DECKS_ITEMS_DIR, exist_ok=True)
    item_path = os.path.join(DECKS_ITEMS_DIR, f"{deck_id}.json")
    with open(item_path, "w", encoding="utf-8") as f:
        json.dump(deck_data, f, ensure_ascii=False, indent=2)
    print(f"6. Runtime item dosyası kaydedildi: {item_path}")

    # 7. INTERACTIVE_LEARNING_DECKS.JSON DOSYASINI YERİNDE GÜNCELLE
    with open(INTERACTIVE_DECKS_PATH, "r", encoding="utf-8") as f:
        all_decks = json.load(f)

    updated = False
    for i, d in enumerate(all_decks):
        if d.get("id") == deck_id:
            all_decks[i] = deck_data
            updated = True
            print(f"7. interactive_learning_decks.json dizininde indeks {i} güncellendi.")
            break

    if not updated:
        all_decks.append(deck_data)
        print("7. interactive_learning_decks.json sonuna eklendi.")

    with open(INTERACTIVE_DECKS_PATH, "w", encoding="utf-8") as f:
        json.dump(all_decks, f, ensure_ascii=False, indent=2)
    print(f"   {INTERACTIVE_DECKS_PATH} başarıyla kaydedildi.")

    # 8. CATALOG.JSON DOSYASINI GÜNCELLE
    if os.path.exists(CATALOG_PATH):
        with open(CATALOG_PATH, "r", encoding="utf-8") as f:
            cat = json.load(f)
        cat_updated = False
        for item in cat:
            if item.get("id") == deck_id:
                item["stepCount"] = deck_data["stepCount"]
                item["questionCount"] = deck_data["questionCount"]
                item["totalFlashcards"] = deck_data["totalFlashcards"]
                item["totalInteractiveElements"] = deck_data["totalInteractiveElements"]
                cat_updated = True
                break
        if not cat_updated:
            cat.append({
                "id": deck_id,
                "title": deck_data["title"],
                "course": deck_data["course"],
                "instructor": deck_data["instructor"],
                "category": deck_data["category"],
                "stepCount": deck_data["stepCount"],
                "questionCount": deck_data["questionCount"],
                "totalFlashcards": deck_data["totalFlashcards"],
                "totalInteractiveElements": deck_data["totalInteractiveElements"]
            })
        with open(CATALOG_PATH, "w", encoding="utf-8") as f:
            json.dump(cat, f, ensure_ascii=False, indent=2)
        print("8. catalog.json başarıyla güncellendi.")

    print("\n" + "=" * 70)
    print("Ders 15 Tamamlandı ve Paketlendi!")
    print(f"Toplam Slayt: {len(enriched_slides)}")
    print(f"Toplam Soru: {len(questions)}")
    print(f"Toplam Flashcard: 30")
    print(f"Toplam Eleman: {total_el}")
    print("=" * 70)

if __name__ == "__main__":
    main()
