#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)
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

from scripts.k1_12_deck_data.helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)
from scripts.k1_12_deck_data.section_1 import get_section_1_slides
from scripts.k1_12_deck_data.section_2 import get_section_2_slides
from scripts.k1_12_deck_data.section_3 import get_section_3_slides
from scripts.k1_12_deck_data.section_4 import get_section_4_slides
from scripts.k1_12_deck_data.section_5 import get_section_5_slides
from scripts.k1_12_deck_data.section_6 import get_section_6_slides
from scripts.k1_12_deck_data.section_7 import get_section_7_slides
from scripts.k1_12_deck_data.section_8 import get_section_8_slides
from scripts.k1_12_deck_data.section_9 import get_section_9_slides
from scripts.k1_12_deck_data.section_10 import get_section_10_slides

from scripts.enrich_k1_12_elements import enrich_slides

# Dosya yolları
QUESTIONS_FILE = os.path.join(BASE_DIR, "meds/src/data/ornek_sorular/k1/k1-12-enflamasyonun-kimyasal-mediyatorleri.json")
PACKAGE_DIR = os.path.join(BASE_DIR, "meds/src/data/decks/packages/k1-12-enflamasyonun-kimyasal-mediyatorleri")
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
        "İlgili mediyatör yolağını düşününüz",
        "Konuyla ilgili temel biyokimyasal mekanizmayı anımsayınız",
        "Ders notundaki kritik patoloji bilgisini hatırlayınız",
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
                "k1-12-fc-01",
                "Hücresel kökenli preforme mediyatörler ile yeni sentezlenen (de novo) mediyatörlerin temel farkı nedir?",
                "Preforme mediyatörler granüllerde hazır depolanmış olup saniyeler içinde salınır (histamin, serotonin); yeni sentezlenenler ise uyarı sonrası membran lipidlerinden veya gen ekspresyonuyla üretilir (eikozanoidler, sitokinler).",
                "Hazır depolanmış vs yeni üretilen moleküller", "Mediyatör Temelleri"
            ),
            make_flashcard(
                "k1-12-fc-02",
                "Mast hücrelerinden histamin degranülasyonunu başlatan en güçlü immünolojik mekanizma nedir?",
                "Yüzeydeki yüksek afiniteli FcεRI reseptörlerine bağlı spesifik IgE antikorlarının antijenle çapraz bağlanmasıdır.",
                "Tip I aşırı duyarlık reseptör mekanizması", "Mediyatör Temelleri"
            ),
            make_flashcard(
                "k1-12-fc-03",
                "Trombosit granüllerinde depolanan, insanlarda karsinoid tümörlerde aşırı salınarak bronkospazm ve ishale yol açan vazoaktif amin hangisidir?",
                "Serotonindir (5-hidroksitriptamin / 5-HT).",
                "Trombosit kaynaklı diğer vazoaktif amin", "Mediyatör Temelleri"
            )
        ],
        19: [
            make_flashcard(
                "k1-12-fc-04",
                "Membran fosfolipidlerinden araşidonik asidi koparan ve kortikosteroidlerce (lipokortin yoluyla) inhibe edilen tepe enzim hangisidir?",
                "Fosfolipaz A2'dir (PLA2).",
                "Tüm lipid kaskadını başlatan membran enzimi", "Eikozanoid Biyosentezi"
            ),
            make_flashcard(
                "k1-12-fc-05",
                "Endotel kökenli prostasiklin (PGI2) ile trombosit kökenli tromboksan A2 (TXA2) arasındaki vasküler ve hemostatik zıtlık nasıldır?",
                "PGI2 güçlü vazodilatasyon ve trombosit agregasyon inhibisyonu yaparken; TXA2 güçlü vazokonstriksiyon ve trombosit agregasyonu yapar.",
                "Zıt çalışan iki temel vazoaktif eikozanoid", "Eikozanoid Biyosentezi"
            ),
            make_flashcard(
                "k1-12-fc-06",
                "Aspirinin diğer NSAİİ'lerden farklı olarak COX enzimlerini geri dönüşümsüz (irreversibl) bloke etme mekanizması nedir?",
                "COX-1 ve COX-2 aktif bölgesindeki serin rezidüsünü kovalent asetilleyerek trombositin yaşamı boyunca TXA2 sentezini durdurmasıdır.",
                "Kovalent bağla kalıcı enzim inaktivasyonu", "Eikozanoid Biyosentezi"
            )
        ],
        29: [
            make_flashcard(
                "k1-12-fc-07",
                "Nötrofiller için en güçlü endojen kemotaktik ajanlardan biri olan ve lökosit adezyonunu artıran 5-LOX ürünü lökotrien hangisidir?",
                "Lökotrien B4'tür (LTB4).",
                "Kemotaktik nötrofil aktivatörü eikozanoid", "Lipoksijenaz Yolağı"
            ),
            make_flashcard(
                "k1-12-fc-08",
                "Sisteinil lökotrienler (LTC4, LTD4, LTE4) bronş düz kasları üzerinde histamine kıyasla ne kadar güçlü etki gösterir?",
                "Histaminden yaklaşık 1000 kat daha güçlü ve uzun süreli bronkokonstriksiyon ve mukus hipersekresyonu yaparlar.",
                "Astımdaki bin kat güçlü spazm molekülleri", "Lipoksijenaz Yolağı"
            ),
            make_flashcard(
                "k1-12-fc-09",
                "Nötrofil kemotaksisini ve adezyonunu durduran, rezolüsyonu başlatan ve trombosit-lökosit transselüler senteziyle üretilen anti-enflamatuar lipidler hangileridir?",
                "Lipoksinlerdir (LXA4 ve LXB4).",
                "Çözünmeyi başlatan araşidonik asit ürünleri", "Lipoksijenaz Yolağı"
            )
        ],
        39: [
            make_flashcard(
                "k1-12-fc-10",
                "Endotel hücrelerinde E-selektin, ICAM-1 ve VCAM-1 adezyon moleküllerinin ekspresyonunu uyararak lökosit ekstravazasyonunu başlatan iki majör akut sitokin hangisidir?",
                "Tümör Nekroz Faktörü (TNF-α) ve İnterlökin-1'dir (IL-1).",
                "Akut enflamasyonun temel yönetici ikilisi", "Akut Sitokinler"
            ),
            make_flashcard(
                "k1-12-fc-11",
                "İnflamazom kompleksinde (NLRP3) kaspaz-1 tarafından inaktif pro-formundan parçalanarak salgılanan pirojenik sitokin hangisidir?",
                "İnterlökin-1 beta'dır (IL-1β).",
                "Kaspaz-1 bağımlı salınan majör sitokin", "Akut Sitokinler"
            ),
            make_flashcard(
                "k1-12-fc-12",
                "Karaciğer hepatositlerinden CRP, fibrinojen ve serum amiloid A gibi akut faz reaktanlarının sentezini uyaran baş sitokin hangisidir?",
                "İnterlökin-6'dır (IL-6).",
                "Karaciğer akut faz yanıtının primer hormonu", "Akut Sitokinler"
            )
        ],
        49: [
            make_flashcard(
                "k1-12-fc-13",
                "Granülomatöz enflamasyonda epiteloid histiosit oluşumunu ve klasik makrofaj (M1) aktivasyonunu sağlayan majör Th1 sitokini hangisidir?",
                "İnterferon-gama'dır (IFN-γ).",
                "Klasik makrofaj aktivasyonunun anahtar molekülü", "Kronik Sitokinler ve Kemokinler"
            ),
            make_flashcard(
                "k1-12-fc-14",
                "Akut enflamasyon odağına özellikle nötrofilleri çağıran, CXCR1 ve CXCR2 reseptörlerine bağlanan CXC tipi majör kemokin hangisidir?",
                "İnterlökin-8'dir (CXCL8).",
                "Nötrofil kemotaksisinin en spesifik kemokini", "Kronik Sitokinler ve Kemokinler"
            ),
            make_flashcard(
                "k1-12-fc-15",
                "HIV-1 virüsünün lenfositlere ve makrofajlara girişte koreseptör olarak kullandığı iki kemokin reseptörü hangileridir?",
                "Makrofajlar için CCR5, T lenfositler için CXCR4 reseptörleridir.",
                "Viral füzyonda kullanılan iki kemokin reseptörü", "Kronik Sitokinler ve Kemokinler"
            )
        ],
        59: [
            make_flashcard(
                "k1-12-fc-16",
                "Kompleman kaskadının klasik yol aktivasyonunu başlatan immünglobulin sınıfları ve bağlanan ilk kompleman molekülü nedir?",
                "IgM veya IgG antikorlarına C1q molekülünün bağlanmasıyla tetiklenir.",
                "Antikor bağımlı klasik başlangıç kompleksi", "Kompleman Sistemi"
            ),
            make_flashcard(
                "k1-12-fc-17",
                "Kompleman aktivasyonu sırasında açığa çıkan en güçlü anaflatoksin ve nötrofil kemoatraktanı olan peptit hangisidir?",
                "C5a'dır (ardından C3a ve C4a gelir).",
                "Kemotaktik ve mast hücresi patlatan en güçlü parça", "Kompleman Sistemi"
            ),
            make_flashcard(
                "k1-12-fc-18",
                "Bakteri veya yabancı partikül yüzeyine kovalent bağlanarak fagositlerdeki CR1 reseptörleriyle opsonizasyon sağlayan kompleman fragmanı hangisidir?",
                "C3b'dir (ayrıca iC3b).",
                "Majör opsonin kompleman parçası", "Kompleman Sistemi"
            )
        ],
        69: [
            make_flashcard(
                "k1-12-fc-19",
                "Eritrosit yüzeyinde GPI çıpasıyla tutunan, kompleman lizisine karşı koruma sağlayan ve eksikliğinde PNH gelişen moleküller hangileridir?",
                "CD55 (DAF - Decay Accelerating Factor) ve CD59'dur (MIRL - Membran İnhibitörü).",
                "PNH'de eksik olan iki yüzey proteini", "Düzenleyiciler ve Kininler"
            ),
            make_flashcard(
                "k1-12-fc-20",
                "C1 esteraz inhibitör (C1-INH) eksikliğinde gelişen Herediter Anjiyoödem tablosunda hayatı tehdit eden laringeal ödemden sorumlu baş mediyatör hangisidir?",
                "Bradikinindir.",
                "Histaminik olmayan anjiyoödem peptidi", "Düzenleyiciler ve Kininler"
            ),
            make_flashcard(
                "k1-12-fc-21",
                "Bradikininin yıkımından sorumlu olan ve inhibitörleri (antihipertansif ACEİ) kullanıldığında kuru öksürük ve anjiyoödeme yol açan enzim hangisidir?",
                "Anjiyotensin Dönüştürücü Enzimdir (ACE / Kininaz II).",
                "Bradikinini inaktive eden vasküler enzim", "Düzenleyiciler ve Kininler"
            )
        ],
        79: [
            make_flashcard(
                "k1-12-fc-22",
                "Venüler permeabiliteyi artırma gücü histaminden 10.000 kat daha fazla olan fosfolipid kaynaklı mediyatör hangisidir?",
                "Trombosit Aktive Edici Faktördür (PAF).",
                "Asetil-gliseril-eter türevi bioaktif lipid", "PAF, NO ve Nöropeptitler"
            ),
            make_flashcard(
                "k1-12-fc-23",
                "Damar endotelinde Ca2+/kalmodulin bağımlı çalışan ve fizyolojik vazodilatasyonu sağlayan NO sentaz izoformu hangisidir?",
                "eNOS'tur (Endotelyal Nitrik Oksit Sentaz / NOS3).",
                "Damar tonusunu koruyan bazal enzim", "PAF, NO ve Nöropeptitler"
            ),
            make_flashcard(
                "k1-12-fc-24",
                "C tipi miyelinsiz duyusal sinir uçlarından salınarak nörojenik enflamasyon ve ağrı iletimini sağlayan temel nöropeptit hangisidir?",
                "P Maddesidir (Substance P).",
                "Nosiseptif iletimin majör nöropeptidi", "PAF, NO ve Nöropeptitler"
            )
        ],
        89: [
            make_flashcard(
                "k1-12-fc-25",
                "Dokuda biriken PGE2'nin lökositlerde 15-LOX enzimini indükleyerek pro-enflamatuar LT'lerden lipoksinlere geçiş sağlamasına ne ad verilir?",
                "Eikozanoid sınıf değişimidir (lipid mediator class switching).",
                "Yangıdan çözünmeye enzimatik makas değişimi", "Rezolüsyon ve Sepsis"
            ),
            make_flashcard(
                "k1-12-fc-26",
                "Makrofajların apoptotik nötrofilleri sessizce fagositozla temizlemesi (eferositoz) sonrasında salgılanan iki anti-enflamatuar ve onarıcı sitokin hangisidir?",
                "İnterlökin-10 (IL-10) ve TGF-beta'dır (TGF-β).",
                "Enflamasyonu söndürüp fibrozisi başlatan ikili", "Rezolüsyon ve Sepsis"
            ),
            make_flashcard(
                "k1-12-fc-27",
                "Karaciğerde IL-6 uyarısıyla sentezlenen, kısa yarı ömrüyle akut alevlenmelerin en hassas izlem göstergesi olan akut faz reaktanı nedir?",
                "C-Reaktif Proteindir (CRP).",
                "Saatler içinde fırlayıp hızla düşen protein", "Rezolüsyon ve Sepsis"
            )
        ],
        100: [
            make_flashcard(
                "k1-12-fc-28",
                "Anti-TNF monoklonal antikorlar (infliksimab, adalimumab) başlanmadan önce granülom stabilitesinin bozulması riski nedeniyle mutlaka taranması gereken enfeksiyon nedir?",
                "Latent tüberküloz enfeksiyonudur (tüberküloz reaktivasyon riski).",
                "Kazeifiye odağın patlamasına yol açan basil riski", "Bütüncül Entegrasyon"
            ),
            make_flashcard(
                "k1-12-fc-29",
                "CAPS ve kolşisine dirençli FMF ataklarında kullanılan rekombinant IL-1 reseptör antagonisti biyolojik ajan hangisidir?",
                "Anakinradır (IL-1Ra).",
                "IL-1 reseptör blokeri ilaç adı", "Bütüncül Entegrasyon"
            ),
            make_flashcard(
                "k1-12-fc-30",
                "Paroksismal Noktürnal Hemoglobinüri (PNH) tedavisinde C5 bölünmesini engelleyerek membran atak kompleksi oluşumunu durduran monoklonal antikor hangisidir?",
                "Ekulizumabdır (tedavi öncesi meningokok aşısı şarttır).",
                "Anti-C5 hümanize antikor adı", "Bütüncül Entegrasyon"
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
    print("Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)")
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
            q_id = q.get("id") or f"k1-12-q{len(questions)+1:02d}"
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

        # Temizlik: Noktalama kontrolleri
        for elem in slide.get("elements", []):
            if elem.get("type") == "cloze_masking":
                elem["hint"] = sanitize_hint(elem.get("hint", ""), elem.get("maskedTerm", ""))
            elif elem.get("type") == "interactive_table":
                for row in elem.get("tableRows", []):
                    for cell in row.get("cells", []):
                        if cell.get("isMasked"):
                            cell["hint"] = sanitize_hint(cell.get("hint", ""), cell.get("text", ""))

    print("3. Flashcardlar ve sorular slaytlara dağıtıldı, ipuçları sanitize edildi.")

    # 4. ÇEŞİTLİLİK KONTROLÜ
    type_counts = Counter()
    total_elements = 0
    for s in enriched_slides:
        for el in s.get("elements", []):
            type_counts[el["type"]] += 1
            total_elements += 1

    print("\n--- İNTERAKTİF ELEMAN DAĞILIMI ---")
    min_pct = 100.0
    for el_type, count in sorted(type_counts.items()):
        pct = (count / total_elements) * 100
        if pct < min_pct:
            min_pct = pct
        print(f"  {el_type:20s}: {count:3d} ({pct:5.2f}%)")
    print(f"Toplam Eleman: {total_elements} (Slayt başına {total_elements/100:.2f} eleman)")
    assert min_pct >= 8.0, f"HATA: En az bir eleman %8.0 altında kaldı! (Min: {min_pct:.2f}%)"
    print(f"BAŞARILI: Tüm 7 eleman tipi >= %8.0 şartını sağlıyor! (En düşük: %{min_pct:.2f})")

    # 5. DESTE METAVERİSİ VE NESNESİ
    deck_id = "k1p-k1-12-enflamasyonun-kimyasal-mediyatorleri"
    deck_title = "Enflamasyonun Kimyasal Mediyatörleri"
    deck_description = "Hücresel ve plazma kökenli kimyasal mediyatörler, histamin, serotonin, araşidonik asit metabolitleri (prostaglandinler, lökotrienler, lipoksinler), sitokinler, kompleman, kinin sistemleri, PAF, NO, aktif rezolüsyon ve hedefe yönelik biyolojik tedavilerin 100 slaytlık tam entegre destesi."

    deck_obj = {
        "id": deck_id,
        "title": deck_title,
        "description": deck_description,
        "course": "Tıbbi Patoloji",
        "committee": "Kurul 1 - Ürogenital ve Obstetrik Kurulu",
        "totalSlides": 100,
        "duration": "180 dk",
        "tags": [
            "Enflamasyon", "Kimyasal Mediyatörler", "Histamin", "Eikozanoidler",
            "Prostaglandinler", "Lökotrienler", "Sitokinler", "Kompleman", "Patoloji"
        ],
        "slides": enriched_slides,
        "questions": questions
    }

    # 6. MULTI-FORMAT PAKETİ OLUŞTUR (meds/src/data/decks/packages/<deck-slug>/)
    os.makedirs(PACKAGE_DIR, exist_ok=True)

    # 6a. manifest.json
    manifest_data = {
        "id": deck_id,
        "title": deck_title,
        "version": "2.0.0",
        "formatVersion": "1.0",
        "author": "Prof. Dr. Hikmet Keleş",
        "course": "Tıbbi Patoloji",
        "committee": "Kurul 1",
        "slideCount": 100,
        "questionCount": len(questions),
        "totalElements": total_elements,
        "elementDistribution": {k: {"count": v, "percentage": round((v/total_elements)*100, 2)} for k, v in type_counts.items()},
        "files": {
            "structure": "structure.xml",
            "content": "content.md",
            "blocks": "blocks.html"
        }
    }
    with open(os.path.join(PACKAGE_DIR, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, ensure_ascii=False, indent=2)

    # 6b. structure.xml
    root_xml = ET.Element("learningDeck", attrib={"id": deck_id, "title": deck_title})
    meta_xml = ET.SubElement(root_xml, "metadata")
    ET.SubElement(meta_xml, "course").text = deck_obj["course"]
    ET.SubElement(meta_xml, "committee").text = deck_obj["committee"]
    ET.SubElement(meta_xml, "slideCount").text = "100"

    slides_xml = ET.SubElement(root_xml, "slides")
    for s in enriched_slides:
        s_el = ET.SubElement(slides_xml, "slide", attrib={"id": s["id"], "title": s["title"]})
        ET.SubElement(s_el, "content").text = s["content"]
        elems_xml = ET.SubElement(s_el, "interactiveElements")
        for el in s.get("elements", []):
            ET.SubElement(elems_xml, "element", attrib={"type": el["type"]})
        if s.get("flashcards"):
            fc_xml = ET.SubElement(s_el, "flashcards")
            for fc in s["flashcards"]:
                ET.SubElement(fc_xml, "flashcard", attrib={"id": fc["id"], "front": fc["front"]})

    rough_xml = ET.tostring(root_xml, encoding="utf-8")
    reparsed_xml = minidom.parseString(rough_xml)
    with open(os.path.join(PACKAGE_DIR, "structure.xml"), "w", encoding="utf-8") as f:
        f.write(reparsed_xml.toprettyxml(indent="  "))

    # 6c. content.md
    md_lines = [
        f"# {deck_title}",
        f"**Ders:** {deck_obj['course']} | **Kurul:** {deck_obj['committee']}",
        f"*{deck_description}*",
        "",
        "---",
        ""
    ]
    for idx, s in enumerate(enriched_slides, start=1):
        md_lines.append(f"## Slayt {idx}: {s['title']}")
        md_lines.append(s['content'])
        md_lines.append("")
        if s.get("flashcards"):
            md_lines.append("### 🧠 Kontrol Noktası Akıl Kartları")
            for fc in s["flashcards"]:
                md_lines.append(f"- **Soru:** {fc['front']}")
                md_lines.append(f"  - **Cevap:** {fc['back']}")
                if fc.get("hint"):
                    md_lines.append(f"  - *İpucu:* {fc['hint']}")
            md_lines.append("")
        md_lines.append("---")
        md_lines.append("")

    with open(os.path.join(PACKAGE_DIR, "content.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    # 6d. blocks.html
    html_lines = [
        "<!DOCTYPE html>",
        "<html lang='tr'>",
        "<head>",
        "  <meta charset='utf-8'>",
        f"  <title>{deck_title}</title>",
        "  <style>",
        "    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; max-width: 900px; margin: 0 auto; padding: 20px; color: #1e293b; }",
        "    .slide { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 24px; margin-bottom: 24px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }",
        "    .slide-title { color: #0f172a; margin-top: 0; font-size: 1.4rem; border-bottom: 2px solid #3b82f6; padding-bottom: 8px; }",
        "    .checkpoint { background: #f0fdf4; border-color: #86efac; }",
        "    .checkpoint .slide-title { border-color: #22c55e; color: #166534; }",
        "    .flashcard { background: #f8fafc; border-left: 4px solid #6366f1; padding: 12px 16px; margin: 12px 0; border-radius: 0 8px 8px 0; }",
        "    .element-tag { display: inline-block; background: #e0f2fe; color: #0369a1; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem; margin-right: 6px; margin-top: 8px; }",
        "  </style>",
        "</head>",
        "<body>",
        f"  <h1>{deck_title}</h1>",
        f"  <p><strong>Kurul:</strong> {deck_obj['committee']} | <strong>Ders:</strong> {deck_obj['course']}</p>",
        f"  <p>{deck_description}</p>",
        "  <hr/>"
    ]
    for idx, s in enumerate(enriched_slides, start=1):
        is_cp = "checkpoint" if "[TEKRAR SAYFASI" in s["title"] else ""
        html_lines.append(f"  <div class='slide {is_cp}' id='slide-{idx}'>")
        html_lines.append(f"    <h2 class='slide-title'>{idx}. {s['title']}</h2>")
        html_lines.append(f"    <div class='slide-content'><p>{s['content'].replace(chr(10), '<br/>')}</p></div>")
        if s.get("elements"):
            html_lines.append("    <div class='slide-elements'>")
            for el in s["elements"]:
                html_lines.append(f"      <span class='element-tag'>{el['type']}</span>")
            html_lines.append("    </div>")
        if s.get("flashcards"):
            html_lines.append("    <div class='flashcards-container'>")
            html_lines.append("      <h3>Akıl Kartları</h3>")
            for fc in s["flashcards"]:
                html_lines.append("      <div class='flashcard'>")
                html_lines.append(f"        <strong>S:</strong> {fc['front']}<br/>")
                html_lines.append(f"        <strong>C:</strong> {fc['back']}")
                html_lines.append("      </div>")
            html_lines.append("    </div>")
        html_lines.append("  </div>")

    html_lines.append("</body>")
    html_lines.append("</html>")
    with open(os.path.join(PACKAGE_DIR, "blocks.html"), "w", encoding="utf-8") as f:
        f.write("\n".join(html_lines))

    print(f"4. Multi-format paketi başarıyla yazıldı: {PACKAGE_DIR}")

    # 7. RUNTIME ITEM DOSYASI (meds/src/data/decks/items/<deck-id>.json)
    os.makedirs(DECKS_ITEMS_DIR, exist_ok=True)
    item_path = os.path.join(DECKS_ITEMS_DIR, f"{deck_id}.json")
    with open(item_path, "w", encoding="utf-8") as f:
        json.dump(deck_obj, f, ensure_ascii=False, indent=2)
    print(f"5. Runtime item dosyası kaydedildi: {item_path}")

    # 8. MASTER INTERACTIVE_LEARNING_DECKS.JSON GÜNCELLE
    if os.path.exists(INTERACTIVE_DECKS_PATH):
        with open(INTERACTIVE_DECKS_PATH, "r", encoding="utf-8") as f:
            all_decks = json.load(f)
        
        found_idx = -1
        for i, d in enumerate(all_decks):
            if d.get("id") == deck_id:
                found_idx = i
                break
        
        if found_idx >= 0:
            all_decks[found_idx] = deck_obj
            print(f"6. interactive_learning_decks.json içinde indeks {found_idx} yerinde güncellendi.")
        else:
            all_decks.append(deck_obj)
            print(f"6. interactive_learning_decks.json sonuna yeni deste eklendi.")
            
        with open(INTERACTIVE_DECKS_PATH, "w", encoding="utf-8") as f:
            json.dump(all_decks, f, ensure_ascii=False, indent=2)
        print("   interactive_learning_decks.json başarıyla kaydedildi.")

    # 9. CATALOG.JSON GÜNCELLE
    if os.path.exists(CATALOG_PATH):
        with open(CATALOG_PATH, "r", encoding="utf-8") as f:
            catalog = json.load(f)
        
        cat_item = {
            "id": deck_id,
            "title": deck_title,
            "description": deck_description,
            "course": deck_obj["course"],
            "committee": deck_obj["committee"],
            "totalSlides": 100,
            "questionCount": len(questions),
            "elementCount": total_elements,
            "duration": "180 dk",
            "packagePath": f"packages/k1-12-enflamasyonun-kimyasal-mediyatorleri",
            "itemPath": f"items/{deck_id}.json"
        }
        
        c_found = False
        if isinstance(catalog, list):
            for i, c in enumerate(catalog):
                if c.get("id") == deck_id:
                    catalog[i] = cat_item
                    c_found = True
                    break
            if not c_found:
                catalog.append(cat_item)
        elif isinstance(catalog, dict) and "decks" in catalog:
            for i, c in enumerate(catalog["decks"]):
                if c.get("id") == deck_id:
                    catalog["decks"][i] = cat_item
                    c_found = True
                    break
            if not c_found:
                catalog["decks"].append(cat_item)
                
        with open(CATALOG_PATH, "w", encoding="utf-8") as f:
            json.dump(catalog, f, ensure_ascii=False, indent=2)
        print("7. catalog.json başarıyla güncellendi.")

    print("\n" + "=" * 70)
    print("Ders 12 Multi-Format Öğrenme Destesi Başarıyla Tamamlandı!")
    print("=" * 70)

if __name__ == "__main__":
    main()
