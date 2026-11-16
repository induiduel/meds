#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)
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

from scripts.k1_14_deck_data.helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)
from scripts.k1_14_deck_data.section_1 import get_section_1_slides
from scripts.k1_14_deck_data.section_2 import get_section_2_slides
from scripts.k1_14_deck_data.section_3 import get_section_3_slides
from scripts.k1_14_deck_data.section_4 import get_section_4_slides
from scripts.k1_14_deck_data.section_5 import get_section_5_slides
from scripts.k1_14_deck_data.section_6 import get_section_6_slides
from scripts.k1_14_deck_data.section_7 import get_section_7_slides
from scripts.k1_14_deck_data.section_8 import get_section_8_slides
from scripts.k1_14_deck_data.section_9 import get_section_9_slides
from scripts.k1_14_deck_data.section_10 import get_section_10_slides

from scripts.enrich_k1_14_elements import enrich_slides

# Dosya yolları
QUESTIONS_FILE = os.path.join(BASE_DIR, "meds/src/data/ornek_sorular/k1/k1-14-salgin-hastaliklarda-kontrol-ve-korunma-yontemleri.json")
PACKAGE_DIR = os.path.join(BASE_DIR, "meds/src/data/decks/packages/k1-14-salgin-hastaliklarda-kontrol-ve-korunma-yontemleri")
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
        "İlgili halk sağlığı ilkesini anımsayınız",
        "Ders notundaki epidemiyoloji kuralını düşününüz",
        "Salgın kontrol prensibini hatırlayınız",
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
                "k1-14-fc-01",
                "21. yüzyılda insanlarda yeni ortaya çıkan (emerging) patojenlerin yaklaşık yüzde kaçı hayvan kaynaklıdır (zoonotiktir)?",
                "Yaklaşık %70'i hayvan kaynaklıdır.",
                "Omurgalı canlılardan insana geçiş payı", "21. Yüzyıl Tehditleri"
            ),
            make_flashcard(
                "k1-14-fc-02",
                "1970'lerden bu yana tıp dünyasında yaklaşık kaç yeni insan patojeni tanımlanmıştır?",
                "1500'den fazla yeni patojen tanımlanmıştır.",
                "Keşfedilen mikrop miktarı", "21. Yüzyıl Tehditleri"
            ),
            make_flashcard(
                "k1-14-fc-03",
                "2009 influenza (domuz gribi) pandemisinde virüsün tüm kıtalara yayılma süresi yaklaşık ne kadar olmuştur?",
                "9 aydan daha kısa sürede tüm kıtalara yayılmıştır.",
                "Grip salgınının dünya turu süresi", "21. Yüzyıl Tehditleri"
            )
        ],
        19: [
            make_flashcard(
                "k1-14-fc-04",
                "Salgınlara hazırlığın üç temel sacayağı nelerdir?",
                "İyi bir sürveyans sistemi, sağlıklı çevre ve bilimsel yatırım ile sağlık sistemleridir.",
                "Savunmanın üç sacayağı", "Salgına Hazırlık ve Tek Sağlık"
            ),
            make_flashcard(
                "k1-14-fc-05",
                "İnsan, hayvan ve çevre sağlığının birbirinden ayrılamaz tek bir bütün olduğunu savunan küresel halk sağlığı vizyonu nedir?",
                "Tek Sağlık (One Health) yaklaşımıdır.",
                "Ekolojik tıp konsepti", "Salgına Hazırlık ve Tek Sağlık"
            ),
            make_flashcard(
                "k1-14-fc-06",
                "Salgınların erken tespitinde ilk alarmı veren en kritik ve vazgeçilmez aktör kimdir?",
                "Klinik ortamda olağan dışı durumu fark eden uyanık klinisyendir.",
                "İlk şüpheyi duyan tıp doktoru", "Salgına Hazırlık ve Tek Sağlık"
            )
        ],
        29: [
            make_flashcard(
                "k1-14-fc-07",
                "Bir salgının doğal seyrindeki dört epidemik faz sırasıyla hangileridir?",
                "Giriş, Lokal Yayılım, Amplifikasyon ve Azalma fazlarıdır.",
                "Dört kronolojik basamak", "Epidemik Fazlar ve Sınırlama"
            ),
            make_flashcard(
                "k1-14-fc-08",
                "Salgın yönetiminde 'sınırlama' (containment) müdahalesi tam olarak ne zaman başlatılmalıdır?",
                "İlk vaka teşhis edildiği anda derhal başlatılmalıdır.",
                "İndeks hastanın belirlenmesiyle eşzamanlı", "Epidemik Fazlar ve Sınırlama"
            ),
            make_flashcard(
                "k1-14-fc-09",
                "Salgının amplifikasyon fazında sağlık sisteminin çökmesini önlemek için uygulanan ana strateji nedir?",
                "Kontrol ve Etkiyi Azaltma (Mitigation) stratejisidir.",
                "Eğriyi yataylaştırma hamlesi", "Epidemik Fazlar ve Sınırlama"
            )
        ],
        39: [
            make_flashcard(
                "k1-14-fc-10",
                "Bir enfeksiyonun tanımlı belirli bir coğrafi bölgede halk sağlığı sorunu olmaktan çıkarılmasına ne denir?",
                "Eliminasyondur (bölgesel yok etme).",
                "Lokal başarı kavramı", "Eliminasyon ve Eradikasyon"
            ),
            make_flashcard(
                "k1-14-fc-11",
                "Bir patojenin yol açtığı enfeksiyonun görülme sıklığının dünya çapında kalıcı olarak sıfırlanmasına ne ad verilir?",
                "Eradikasyondur (küresel kalıcı yok oluş).",
                "Gezegen çapında bitiş", "Eliminasyon ve Eradikasyon"
            ),
            make_flashcard(
                "k1-14-fc-12",
                "İnsanlık tarihinde küresel olarak eradike edilmiş tek insan enfeksiyon hastalığı hangisidir?",
                "Çiçek hastalığıdır (Smallpox - Variola).",
                "Tarihte yok edilmiş tek virüs marazı", "Eliminasyon ve Eradikasyon"
            )
        ],
        49: [
            make_flashcard(
                "k1-14-fc-13",
                "Kapsamlı bir salgın yanıtının sistemde bulunması zorunlu olan dört temel özelliği nelerdir?",
                "Kurumlar arası koordinasyon, tam sağlık enformasyonu, doğru risk iletişimi ve eksiksiz sağlık müdahaleleridir.",
                "Dörtlü operasyonel mimari", "Salgın Yanıtının Dört Bileşeni"
            ),
            make_flashcard(
                "k1-14-fc-14",
                "Salgın yönetiminde paydaşların bir arada karar aldığı özel fiziksel komuta merkezine ne ad verilir?",
                "Acil Operasyon Merkezidir (ASOM / EOC).",
                "Kriz komuta karargahı", "Salgın Yanıtının Dört Bileşeni"
            ),
            make_flashcard(
                "k1-14-fc-15",
                "Epidemiyolojide sürveyans verilerinin toplandığı ve analiz edildiği üç kutsal eksen nedir?",
                "Kişi, zaman ve yer değişkenleridir.",
                "Kim, ne vakit ve nerede soruları", "Salgın Yanıtının Dört Bileşeni"
            )
        ],
        59: [
            make_flashcard(
                "k1-14-fc-16",
                "Salgın sırasında patojenle birlikte yanlış, gereksiz ve panik yaratan abartılı bilgilerin kontrolsüz yayılmasına ne ad verilir?",
                "İnfodemidir.",
                "Yalan haber bolluğu", "Risk İletişimi ve İnfodemi"
            ),
            make_flashcard(
                "k1-14-fc-17",
                "İnfodemiyle mücadelede Dünya Sağlık Örgütü'nün belirlediği üç temel eylem ilkesi nedir?",
                "Konuş, dinle ve dedikoduları engelle prensipleridir.",
                "Üçlü iletişim formülü", "Risk İletişimi ve İnfodemi"
            ),
            make_flashcard(
                "k1-14-fc-18",
                "21. yüzyılda uzman görüşünün halk tarafından benimsenmesi için öncelikle neyin tesis edilmesi şarttır?",
                "Güven tesis edilmeli ve toplumun kaygıları dinlenmelidir.",
                "Karşılıklı inanç ve empati zemini", "Risk İletişimi ve İnfodemi"
            )
        ],
        69: [
            make_flashcard(
                "k1-14-fc-19",
                "DSÖ verilerine göre difteri-tetanoz-boğmaca (DTP) kombine aşısı küresel çocukların yaklaşık yüzde kaçını korur?",
                "Çocukların yaklaşık %86'sını korumaktadır.",
                "Gezegen genelindeki bebek kalkanı", "Sağlık İşgücü ve Klinik Bakım"
            ),
            make_flashcard(
                "k1-14-fc-20",
                "Sağlık çalışanlarının KKE kullanımı sırasında en yüksek bulaş riskinin yaşandığı kritik evre hangisidir?",
                "KKE'yi çıkarma (doffing) aşamasıdır.",
                "Tulum ve maskeyi soyunma periyodu", "Sağlık İşgücü ve Klinik Bakım"
            ),
            make_flashcard(
                "k1-14-fc-21",
                "2014 Batı Afrika Ebola salgınında spesifik ilaç olmadan sadece iyi destekleyici bakımla ölüm oranı yüzde kaçtan kaça düşmüştür?",
                "Ölüm oranı yaklaşık %75'ten %33'e gerilemiştir.",
                "Batı Afrika kliniğindeki istatistiki düşüş", "Sağlık İşgücü ve Klinik Bakım"
            )
        ],
        79: [
            make_flashcard(
                "k1-14-fc-22",
                "Kırım-Kongo Kanamalı Ateşi'nin (KKKA) başlıca bulaş yolu ve omurgasız vektörü nedir?",
                "Hyalomma cinsi keneler ve enfekte hayvan kanı/dokusuyla temastır.",
                "Kırım-Kongo vektörü", "Bulaş Yolları ve Önleme"
            ),
            make_flashcard(
                "k1-14-fc-23",
                "Vibrio cholerae bakterisinin yol açtığı kolera salgınlarında temel bulaş yolu nedir?",
                "Fekal-oral yol ve kontamine içme sularıdır.",
                "Koleranın taşınma ortamı", "Bulaş Yolları ve Önleme"
            ),
            make_flashcard(
                "k1-14-fc-24",
                "Kanamalı ateş salgınlarında cesetlerden kaynaklanan süper-bulaşları önlemek için uygulanan defin standardı nedir?",
                "Güvenli ve Onurlu Defindir (Safe and Dignified Burial).",
                "Dini inançlara saygılı cenaze gömme usulü", "Bulaş Yolları ve Önleme"
            )
        ],
        89: [
            make_flashcard(
                "k1-14-fc-25",
                "Tamamen duyarlı bir toplumda enfekte bir vakanın bulaştırdığı ortalama ikincil vaka sayısına ne ad verilir?",
                "Temel üreme sayısıdır (R0).",
                "Sıfır anındaki bulaştırma gücü", "Aşılar ve İmmünizasyon"
            ),
            make_flashcard(
                "k1-14-fc-26",
                "Salgın kontrolünde vakanın doğrudan ve dolaylı temaslılarını hızla aşılayarak bulaşı odakta sınırlandırma stratejisine ne denir?",
                "Halka aşılamadır (Ring vaccination).",
                "Çember biçiminde koruma", "Aşılar ve İmmünizasyon"
            ),
            make_flashcard(
                "k1-14-fc-27",
                "Rutin çocukluk çağı aşılarının saklanması ve taşınması gereken standart soğuk zincir sıcaklık aralığı nedir?",
                "+2°C ile +8°C arasındadır.",
                "Standart soğutucu dolap derecesi", "Aşılar ve İmmünizasyon"
            )
        ],
        100: [
            make_flashcard(
                "k1-14-fc-28",
                "Bulaşıcı hastalığı kesinleşmiş hastaya uygulanan yalıtım ile semptomsuz temaslıya uygulanan kısıtlama arasındaki terim farkı nedir?",
                "Hasta kişiye izolasyon, semptomsuz temaslıya kuluçka süresince karantina uygulanır.",
                "İki farklı ayırma terimi", "Bütüncül Entegrasyon"
            ),
            make_flashcard(
                "k1-14-fc-29",
                "Dünya Sağlık Örgütü tarafından ilan edilen en üst düzey küresel halk sağlığı alarm statüsü nedir?",
                "PHEIC'tir (Uluslararası Öneme Sahip Halk Sağlığı Acil Durumu).",
                "Küresel en üst alarm kodu", "Bütüncül Entegrasyon"
            ),
            make_flashcard(
                "k1-14-fc-30",
                "Salgın sona erdiğinde tüm paydaşların güçlü ve zayıf yönleri analiz ettiği yapılandırılmış öğrenme sürecine ne ad verilir?",
                "Eylem Sonrası İncelemedir (After-Action Review / AAR).",
                "Kriz bitimi sistematik değerlendirme", "Bütüncül Entegrasyon"
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
    print("Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)")
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
            q_id = q.get("id") or f"k1-14-q{len(questions)+1:02d}"
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
    deck_id = "k1p-k1-14-salgin-hastaliklarda-kontrol-ve-korunma-yontemleri"
    deck_data = {
        "id": deck_id,
        "title": "Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri",
        "description": "Bulaşıcı hastalıkların yeniden ortaya çıkışı, hazırlık unsurları, Tek Sağlık yaklaşımı, epidemik fazlar, sınırlama ve mitigasyon, eliminasyon vs eradikasyon, salgın yanıtının 4 temel bileşeni (koordinasyon, enformasyon, risk iletişimi, müdahaleler), infodemi yönetimi, sağlık işgücünün korunması, klinik destekleyici bakım (Ebola %75->%33), bulaş yollarına göre DSÖ müdahaleleri, güvenli ve onurlu defin, aşı matematiği (R0, HIT, halka aşılama), soğuk zincir (+2°C/+8°C), IHR 2005 ve biyoetik entegrasyonu.",
        "course": "Halk Sağlığı",
        "category": "Kurul 1 · 2026-2027 ders paketi",
        "instructor": "Uzm. Dr. Erkay Nacar (Halk Sağlığı ABD)",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "stepCount": len(enriched_slides),
        "questionCount": len(questions),
        "totalFlashcards": 30,
        "totalInteractiveElements": total_el,
        "slides": enriched_slides,
        "questions": questions
    }

    # 5. MULTI-FORMAT PAKETLEME (packages/k1-14-salgin-hastaliklarda-kontrol-ve-korunma-yontemleri)
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

    # 6. RUNTIME ITEM DOSYASI (items/k1p-k1-14-salgin-hastaliklarda-kontrol-ve-korunma-yontemleri.json)
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
    print("Ders 14 Tamamlandı ve Paketlendi!")
    print(f"Toplam Slayt: {len(enriched_slides)}")
    print(f"Toplam Soru: {len(questions)}")
    print(f"Toplam Flashcard: 30")
    print(f"Toplam Eleman: {total_el}")
    print("=" * 70)

if __name__ == "__main__":
    main()
