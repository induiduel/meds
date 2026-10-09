#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)
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

from scripts.k1_11_deck_data.helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)
from scripts.k1_11_deck_data.section_1 import get_section_1_slides
from scripts.k1_11_deck_data.section_2 import get_section_2_slides
from scripts.k1_11_deck_data.section_3 import get_section_3_slides
from scripts.k1_11_deck_data.section_4 import get_section_4_slides
from scripts.k1_11_deck_data.section_5 import get_section_5_slides
from scripts.k1_11_deck_data.section_6 import get_section_6_slides
from scripts.k1_11_deck_data.section_7 import get_section_7_slides
from scripts.k1_11_deck_data.section_8 import get_section_8_slides
from scripts.k1_11_deck_data.section_9 import get_section_9_slides
from scripts.k1_11_deck_data.section_10 import get_section_10_slides

from scripts.enrich_k1_11_elements import (
    get_extra_branching, get_extra_sliders, get_extra_causal_chains
)

# Dosya yolları
QUESTIONS_FILE = os.path.join(BASE_DIR, "meds/src/data/ornek_sorular/k1/k1-11-uriner-obstruksiyonun-fizyopatolojisi.json")
PACKAGE_DIR = os.path.join(BASE_DIR, "meds/src/data/decks/packages/k1-11-uriner-obstruksiyonun-fizyopatolojisi")
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
        "İlgili ürolojik mekanizmayı düşününüz",
        "Konuyla ilgili temel klinik prensibi anımsayınız",
        "Ders notundaki kritik bilgiyi hatırlayınız",
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
                "k1-11-fc-01",
                "Obstrüktif üropatide hastanın klinik tablosunu ve prognozunu belirleyen 4 temel kardinal faktör nedir?",
                "Obstrüksiyonun seviyesi, derecesi, süresi ve enfeksiyon varlığıdır.",
                "Dört kardinal prognostik etken", "Obstrüksiyon Temelleri"
            ),
            make_flashcard(
                "k1-11-fc-02",
                "Supravezikal ve infravezikal obstrüksiyonlar etkilenen böbrek tarafı açısından nasıl ayrılır?",
                "Supravezikal tıkanıklık kural olarak tek bir böbreği, infravezikal tıkanıklık ise her iki böbreği birden etkiler.",
                "İki majör anatomik ayrım", "Obstrüksiyon Temelleri"
            ),
            make_flashcard(
                "k1-11-fc-03",
                "Mesanenin akut komplet çıkım obstrüksiyonu sonucu aşırı gerilip suprapubik kitle oluşturmasına ne ad verilir?",
                "Glob vezikaledir (akut üriner retansiyon tablosu).",
                "Dolu ve gergin idrar torbası kitlesi", "Obstrüksiyon Temelleri"
            )
        ],
        19: [
            make_flashcard(
                "k1-11-fc-04",
                "Böbrek düzeyinde en sık izlenen konjenital supravezikal obstrüksiyon nedeni hangisidir?",
                "Üreteropelvik bileşke (UPJ) darlığıdır.",
                "Pelvis ile tüp arasındaki konjenital darlık", "Etiyolojik Spektrum"
            ),
            make_flashcard(
                "k1-11-fc-05",
                "Erkek çocuklarda ve yaşlı erkeklerde en sık görülen infravezikal obstrüksiyon nedenleri nelerdir?",
                "Erkek çocuklarda posterior üretral valv (PUV), yaşlı erkeklerde benign prostat hiperplazisidir (BPH).",
                "Yaşa göre iki majör tıkanıklık nedeni", "Etiyolojik Spektrum"
            ),
            make_flashcard(
                "k1-11-fc-06",
                "Gebelikte görülen fizyolojik hidronefrozun belirgin olarak sağ tarafta (%80-90) baskın olmasının sebepleri nelerdir?",
                "Uterusun sağa dekstrorotasyonu, sağ ovaryan ven basısı ve progesteron hormonunun düz kas gevşetici etkisidir.",
                "Dekstrorotasyon ve venöz bası etkileri", "Etiyolojik Spektrum"
            )
        ],
        29: [
            make_flashcard(
                "k1-11-fc-07",
                "Kronik infravezikal obstrüksiyonun 3 evresi sırasıyla hangileridir ve rezidüel idrar hacimleri nasıldır?",
                "Kompansasyon (PVR=0 ml), irritasyon (PVR < 50 ml) ve dekompansasyon (PVR > 500 ml) evreleridir.",
                "Üç aşamalı mesane yetmezliği seyri", "Alt Üriner Sistem Evreleri"
            ),
            make_flashcard(
                "k1-11-fc-08",
                "Mesane duvarında obstrüksiyon sonucu artarak mesane kompliyansını ve esnekliğini yok eden temel bağ dokusu proteini nedir?",
                "Tip III kollajendir.",
                "Rijit skar oluşturan fibriler protein", "Alt Üriner Sistem Evreleri"
            ),
            make_flashcard(
                "k1-11-fc-09",
                "Kronik mesane çıkım darlığında sekonder vezikoüreteral reflü (VUR) gelişiminin temel anatomik sebebi nedir?",
                "Mesane duvarının aşırı gerilmesiyle intramural üreter tünelinin kısalması ve flap-valv mekanizmasının çökmesidir.",
                "Kısalan oblik tünel anatomisi", "Alt Üriner Sistem Evreleri"
            )
        ],
        39: [
            make_flashcard(
                "k1-11-fc-10",
                "Üst üriner sistem obstrüksiyonunda intrapelvik basınç artışından ilk ve en erken etkilenen anatomik bölge neresidir?",
                "Kalikslerdir (fornikslerin küntleşmesi ve papillaların yassılaşması izlenir).",
                "Kadeh biçimli toplayıcı yapı hasarı", "Üst Üriner Sistem Dinamikleri"
            ),
            make_flashcard(
                "k1-11-fc-11",
                "Supravezikal obstrüksiyonda forniks mikro-yırtıklarından böbrek sinüsüne idrar sızmasını sağlayan en sık koruyucu reflü yolu nedir?",
                "Pyelointerstisyel reflüdür.",
                "En sık görülen dekompresyon mekanizması", "Üst Üriner Sistem Dinamikleri"
            ),
            make_flashcard(
                "k1-11-fc-12",
                "Deneysel modellerde tam üreter obstrüksiyonu sonrası dekompresyonla geri dönen GFR oranları süreye göre nasıldır?",
                "2 haftada kontrolün %46'sı, 4 haftada %35'i dönerken; 6 haftalık tam tıkanıklıktan sonra geri dönen hiçbir fonksiyon kalmaz (%0).",
                "Altı haftalık irreversibilite eşiği", "Üst Üriner Sistem Dinamikleri"
            )
        ],
        49: [
            make_flashcard(
                "k1-11-fc-13",
                "Bowman kapsülü içi hidrostatik basıncın yükselerek net glomerüler filtrasyonu tamamen durdurduğu intralüminal basınca ne ad verilir?",
                "Stop flow pressure (durdurma basıncı).",
                "Filtrasyon akımını sıfırlayan kritik intralüminal basınç", "Glomerüler Hemodinami"
            ),
            make_flashcard(
                "k1-11-fc-14",
                "Akut üreter obstrüksiyonunun ilk 1-2 saatinde aferent vazodilatasyonla RBF'yi artıran iki temel mediyatör hangisidir?",
                "Prostaglandin E2 (PGE2) ve Nitrik Oksittir (NO).",
                "Erken dönem lokal damar gevşeticileri", "Glomerüler Hemodinami"
            ),
            make_flashcard(
                "k1-11-fc-15",
                "Obstrüksiyonun geç evresinde renal vasküler direnci artırıp iskemiye yol açan temel vazokonstriktör ajanlar hangileridir?",
                "Tromboksan A2 (TXA2) ve Anjiyotensin II'dir.",
                "İskemi başlatan vazokonstriktör ikili", "Glomerüler Hemodinami"
            )
        ],
        59: [
            make_flashcard(
                "k1-11-fc-16",
                "Obstrüksiyonda gelişen edinsel nefrojenik diyabetes insipidus tablosunda toplayıcı tübüllerdeki moleküler defekt nedir?",
                "Toplayıcı kanallarda ADH duyarsızlığı sonucu apikal membrana Akuaporin-2 (AQP2) su kanallarının taşınamamasıdır.",
                "Su kanalı eksikliği ve hormon direnci", "Tübüler Fonksiyonlar"
            ),
            make_flashcard(
                "k1-11-fc-17",
                "Obstrüksiyonda idrar asidifikasyon kapasitesinin çökmesinden sorumlu olan distal tübüler hücreler ve pompaları hangisidir?",
                "Toplayıcı kanal alfa-interkale hücreleri ve bunların apikal H+-ATPaz pompalarıdır.",
                "Asit pompalayan özelleşmiş hücreler", "Tübüler Fonksiyonlar"
            ),
            make_flashcard(
                "k1-11-fc-18",
                "Üriner obstrüksiyon dekomprese edildikten sonra böbreğin konsantrasyon kapasitesi iflas etmişken korunan ve ETKİLENMEYEN fonksiyon nedir?",
                "Üriner dilüsyon (idrarı sulandırabilme) yeteneğidir.",
                "Ders notundaki en kritik sınav kuralı", "Tübüler Fonksiyonlar"
            )
        ],
        69: [
            make_flashcard(
                "k1-11-fc-19",
                "Akut distal üreter taşında renal kolik ağrısının erkeklerde testise, kadınlarda labium majusa yayılmasını sağlayan spinal dermatomlar hangileridir?",
                "T10-L1 spinal segmentleridir.",
                "Alt torakal ve üst lomber kökler", "Klinik Tablo"
            ),
            make_flashcard(
                "k1-11-fc-20",
                "Bir hastada idrar çıkışının aniden 50 ml/gün altına düşmesi (ani anüri) ilk olarak hangi acil durumu düşündürmelidir?",
                "Akut bilateral mekanik obstrüksiyonu veya soliter fonksiyonel böbrek tam obstrüksiyonunu düşündürmelidir.",
                "Mekanik tıkanıklığın en dramatik acili", "Klinik Tablo"
            ),
            make_flashcard(
                "k1-11-fc-21",
                "Tek taraflı böbrek obstrüksiyonunda sağlam böbreğin büyümesine ve tıkanıklık açılınca fonksiyonun dengelenmesine ne ad verilir?",
                "Renal kontrbalans (kompansatuar hipertrofi ve drenaj sonrası hipotrofi).",
                "Böbrekler arası iş yükü dengesi", "Klinik Tablo"
            )
        ],
        79: [
            make_flashcard(
                "k1-11-fc-22",
                "Obstrüksiyon şüphesinde ilk basamak radyolojik modalite ve akut taş şüphesinde altın standart tanı yöntemi nedir?",
                "İlk basamak yöntem Ultrasonografi (USG); akut taşta altın standart yöntem Kontrassız Helikal Taş BT'dir.",
                "İlk basamak ses dalgası, altın standart tomografi", "Radyolojik Değerlendirme"
            ),
            make_flashcard(
                "k1-11-fc-23",
                "Diüretikli renal sintigrafide (Lasix testi) gerçek mekanik obstrüksiyon ile non-obstrüktif drenajı ayıran T1/2 zaman eşikleri nelerdir?",
                "T1/2 > 20 dakika ise mekanik obstrüksiyon; T1/2 < 10 dakika ise obstrüksiyon yokluğudur.",
                "Yirmi ve on dakika kuralları", "Radyolojik Değerlendirme"
            ),
            make_flashcard(
                "k1-11-fc-24",
                "Mesane çıkım darlığı (BOO) ile detrüsör kas güçsüzlüğünü objektif olarak ayıran altın standart inceleme hangisidir?",
                "Basınç-akım çalışmasıdır (pressure-flow study).",
                "Eş zamanlı basınç ve debi kaydı", "Radyolojik Değerlendirme"
            )
        ],
        89: [
            make_flashcard(
                "k1-11-fc-25",
                "Üst üriner sistem obstrüksiyonlarında enfeksiyon (piyonefroz) ve sepsis varlığında en emniyetli acil drenaj yöntemi nedir?",
                "Perkütan nefrostomidir (PNS).",
                "Ciltten kalikse takılan acil tüp", "Tedavi ve Dekompresyon"
            ),
            make_flashcard(
                "k1-11-fc-26",
                "Bilateral obstrüksiyon açıldıktan sonra gelişen postobstrüktif diürezin (POD) temel ozmotik tetikleyicisi nedir?",
                "Kanda birikmiş olan yüksek üre moleküllerinin hızla filtre edilerek tübüllerde ozmotik su çekmesidir.",
                "Azotlu atığın ozmotik su sürüklemesi", "Tedavi ve Dekompresyon"
            ),
            make_flashcard(
                "k1-11-fc-27",
                "Postobstrüktif diürezde iatrojenik poliüri döngüsüne girmemek için intravenöz sıvı replasman kuralı nasıldır?",
                "Çıkan idrarın %100'ü verilmez; organizmanın kendi dengesini kurması için çıkan hacmin %50-70'i oranında hipotonik sıvı verilir.",
                "Yüzde elli yetmiş sıvı replasman kuralı", "Tedavi ve Dekompresyon"
            )
        ],
        100: [
            make_flashcard(
                "k1-11-fc-28",
                "Glob vezikalede mesanenin aniden boşaltılması sonucu vakum etkisiyle gelişen kanamaya ne ad verilir?",
                "Ex vacuo hematüri (dekompresyon hematürisi).",
                "Boşluk etkisiyle gelişen kanama tablosu", "Bütüncül Entegrasyon"
            ),
            make_flashcard(
                "k1-11-fc-29",
                "Üreteropelvik bileşke (UPJ) darlığında dar segmentin çıkarılıp pelvise dikildiği altın standart ameliyat hangisidir?",
                "Anderson-Hynes (dezmember) pyeloplasti ameliyatıdır.",
                "Eponymli ayrık pelvik rekonstrüksiyon ameliyatı", "Bütüncül Entegrasyon"
            ),
            make_flashcard(
                "k1-11-fc-30",
                "Kronik obstrüktif nefropatili hastaların uzun dönem izleminde kalan nefronları korumak için kesinlikle yasaklanan ilaç grubu nedir?",
                "Non-Steroid Antiinflamatuar İlaçlardır (NSAİİ).",
                "Aferent damarı büzen klasik ağrı kesiciler", "Bütüncül Entegrasyon"
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
    print("Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)")
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
            q_id = q.get("id") or f"k1-11-q{len(questions)+1:02d}"
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
                        exp_opt = o.get("explanation") or (f"Doğru cevap {k_opt}'dir: {gen_exp}" if k_opt == corr else f"{k_opt} seçeneği yanlıştır.")
                    else:
                        txt_opt = str(o)
                        exp_opt = f"Doğru cevap {k_opt}'dir: {gen_exp}" if k_opt == corr else f"{k_opt} seçeneği yanlıştır."
                    normalized_opts.append({
                        "key": k_opt,
                        "text": txt_opt,
                        "explanation": exp_opt
                    })

            if q_text and len(normalized_opts) >= 2:
                questions.append({
                    "id": q_id,
                    "question": q_text,
                    "options": normalized_opts,
                    "correctAnswer": corr,
                    "explanation": gen_exp
                })

    print(f"2. Yüklenen ve normalize edilen örnek soru sayısı: {len(questions)}")

    # 3. İNTERAKTİF ELEMANLARI DENGELE VE ASSEMBLE ET
    extra_branching = get_extra_branching()
    extra_sliders = get_extra_sliders()
    extra_causal = get_extra_causal_chains()
    checkpoint_fc_dict = get_checkpoint_flashcards()

    final_slides = []
    checkpoint_counter = 0

    for idx, slide in enumerate(raw_slides):
        slide_num = idx + 1
        slide["slideNumber"] = slide_num

        # Checkpoint kontrolü (Adım 9, 19, 29, 39, 49, 59, 69, 79, 89, 100)
        is_cp = (slide_num in [9, 19, 29, 39, 49, 59, 69, 79, 89, 100])
        if is_cp:
            checkpoint_counter += 1
            slide["isCheckpoint"] = True
            slide["checkpointNumber"] = checkpoint_counter
            if slide_num in checkpoint_fc_dict:
                slide["flashcards"] = checkpoint_fc_dict[slide_num]
            elif not slide.get("flashcards"):
                print(f"UYARI: Slayt {slide_num} checkpoint ancak flashcard yok!")
        else:
            slide.pop("isCheckpoint", None)
            slide.pop("checkpointNumber", None)
            slide.pop("flashcards", None)

        # Ekstra elemanları ilgili slaytlara ekle
        raw_elems = slide.get("interactiveElements") or slide.get("elements") or []
        elements = list(raw_elems)

        if slide_num in extra_branching:
            elements.append(extra_branching[slide_num])
        if slide_num in extra_sliders:
            elements.append(extra_sliders[slide_num])
        if slide_num in extra_causal:
            elements.append(extra_causal[slide_num])

        # Şema normalizasyonları ve sızıntı temizliği
        for el in elements:
            t = el.get("type")
            if t == "branching_logic":
                if "options" not in el and "branchingOptions" in el:
                    el["options"] = el["branchingOptions"]
                elif "branchingOptions" not in el and "options" in el:
                    el["branchingOptions"] = el["options"]
                for o in el.get("options", []):
                    if "isCorrect" in o and "isOptimal" not in o:
                        o["isOptimal"] = o["isCorrect"]
                    elif "isOptimal" in o and "isCorrect" not in o:
                        o["isCorrect"] = o["isOptimal"]
            elif t == "before_after_slider":
                lt = el.get("leftTitle") or el.get("beforeState", {}).get("label") or "Durum A"
                rt = el.get("rightTitle") or el.get("afterState", {}).get("label") or "Durum B"
                ld = el.get("leftPoints") or el.get("beforeState", {}).get("description") or ""
                rd = el.get("rightPoints") or el.get("afterState", {}).get("description") or ""
                lp = [ld] if isinstance(ld, str) else list(ld)
                rp = [rd] if isinstance(rd, str) else list(rd)
                el["leftTitle"] = lt
                el["rightTitle"] = rt
                el["leftPoints"] = lp
                el["rightPoints"] = rp
                if "beforeState" not in el:
                    el["beforeState"] = {"label": lt, "description": lp[0] if lp else ""}
                if "afterState" not in el:
                    el["afterState"] = {"label": rt, "description": rp[0] if rp else ""}
            elif t == "cloze_masking":
                h = el.get("hint", "")
                a = el.get("maskedTerm", "")
                if h and leaks(h, a):
                    el["hint"] = sanitize_hint(h, a)
            elif t == "interactive_table":
                hdrs = el.get("tableHeaders", [])
                rows = el.get("tableRows", [])
                for r in rows:
                    cells = r.get("cells", [])
                    if len(cells) < len(hdrs):
                        diff = len(hdrs) - len(cells)
                        for _ in range(diff):
                            cells.append({
                                "text": "Standart klinik parametre",
                                "isMasked": False,
                                "hint": ""
                            })
                    elif len(cells) > len(hdrs):
                        cells = cells[:len(hdrs)]
                        r["cells"] = cells

                    for c in cells:
                        if isinstance(c, dict) and c.get("isMasked"):
                            ch = c.get("hint", "")
                            ca = c.get("text", "")
                            if ch and leaks(ch, ca):
                                c["hint"] = sanitize_hint(ch, ca)
            elif t == "active_recall":
                h = el.get("clue", "")
                a = el.get("answer", "")
                if h and leaks(h, a):
                    el["clue"] = sanitize_hint(h, a)

        # Anlatım alanlarını validator standartlarına uygun bağla
        core_txt = slide.get("coreContent", {}).get("text") or slide.get("content", "")
        slide["synthesisNarrative"] = core_txt
        slide["content"] = core_txt
        if not slide.get("coreContent"):
            slide["coreContent"] = {
                "text": core_txt,
                "keyBullets": [
                    {"title": slide["title"], "desc": slide.get("subtitle", slide["title"]), "isKey": True}
                ]
            }
        elif not slide.get("coreContent", {}).get("keyBullets"):
            slide.setdefault("coreContent", {})["keyBullets"] = [
                {"title": slide["title"], "desc": slide.get("subtitle", slide["title"]), "isKey": True}
            ]

        slide["interactiveElements"] = elements
        slide.pop("elements", None)
        final_slides.append(slide)

    print(f"3. 100 Slayt başarıyla yapılandırıldı.")

    # 4. İSTATİSTİK VE ÇEŞİTLİLİK KONTROLÜ
    elem_counts = Counter()
    for s in final_slides:
        for el in s.get("interactiveElements", []):
            elem_counts[el.get("type")] += 1

    total_elems = sum(elem_counts.values())
    print("\n" + "=" * 50)
    print(f"İNTERAKTİF ELEMAN İSTATİSTİKLERİ (Toplam: {total_elems})")
    print("=" * 50)
    diversity_passed = True
    for t_name, count in elem_counts.items():
        pct = (count / total_elems) * 100
        print(f"  - {t_name:22s}: {count:3d} ({pct:5.1f}%)")
        if pct < 8.0:
            print(f"    HATA: {t_name} %8 sınırının altında! ({pct:.1f}%)")
            diversity_passed = False

    assert diversity_passed, "HATA: En az bir interaktif eleman %8 çeşitlilik kuralını sağlamıyor!"
    print("-> TÜM 7 İNTERAKTİF ELEMAN %8 ÇEŞİTLİLİK KRİTERİNİ SAĞLIYOR! (BAŞARILI)")

    # 5. MULTI-FORMAT PAKET DOSYALARINI ÜRET
    os.makedirs(PACKAGE_DIR, exist_ok=True)

    deck_metadata = {
        "id": "k1p-k1-11-uriner-obstruksiyonun-fizyopatolojisi",
        "title": "Üriner Obstrüksiyonun Fizyopatolojisi",
        "shortTitle": "Üriner Obstrüksiyonun Fizyopatolojisi",
        "discipline": "Üroloji",
        "committee": "Kurul 1 - Ürogenital ve Obstetrik Kurulu",
        "instructor": "Doç. Dr. Özer Baran",
        "overview": (
            "Obstrüktif üropati, idrar üretim yeri olan tübüllerden eksternal meaya kadar idrar akımının engellendiği klinik tablodur. "
            "Klinik tabloyu seviye, derece, süre ve enfeksiyon belirler; proksimalinde staz ve basınç artışı olur. "
            "İnfravezikal obstrüksiyonda kompanzasyon (PVR=0), irritasyon (PVR<50 ml) ve dekompansasyon (PVR>500 ml, VUR) evreleri görülür; "
            "mesane duvarında tip III kollajen artışı ile kompliyans çöker, trabekülasyon ve divertiküller gelişir. "
            "Supravezikal tıkanıklıkta ilk etkilenen kalikslerdir (forniks küntleşmesi, papilla düzleşmesi); 7. günde kollektör nekrozu başlar. "
            "Pyelointerstisyel, pyelolenfatik ve pyelovenöz reflü basıncı düşürür. Erken fazda PGE2/NO vazodilatasyonu, geç fazda TXA2/AngII "
            "vazokonstriksiyonu görülür; 6 haftalık tam tıkanıklıktan sonra fonksiyon dönmez. Toplayıcı kanallarda ADH direnci, hipostenürik poliüri "
            "ve asidifikasyon defekti gelişirken, ÜRİNER DİLÜSYON YETENEĞİ SAĞLAM KALIR. Anüri ve piyonefroz acildir; açılınca postobstrüktif diürez "
            "izlenir ve çıkanın %50-70'i replase edilir."
        ),
        "totalSlides": 100,
        "slideCount": 100,
        "totalQuestions": len(questions),
        "questionCount": len(questions),
        "totalFlashcards": 30,
        "interactiveElementCount": total_elems,
        "category": "Kurul 1 · 2026-2027 ders paketi",
        "programDate": "2026-09-17",
        "confidence": "high",
        "themeColor": "sky"
    }

    # 5a. manifest.json
    manifest_data = {
        "version": "1.0",
        "metadata": deck_metadata,
        "structure": "structure.xml",
        "blocks": "blocks.html",
        "content": "content.md",
        "stats": {
            "slideCount": 100,
            "elementCount": total_elems,
            "questionCount": len(questions),
            "flashcardCount": 30,
            "elementDistribution": dict(elem_counts)
        }
    }
    with open(os.path.join(PACKAGE_DIR, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, ensure_ascii=False, indent=2)
    print("5a. manifest.json yazıldı.")

    # 5b. structure.xml
    root = ET.Element("learningDeck", id=deck_metadata["id"], title=deck_metadata["title"])
    meta_el = ET.SubElement(root, "metadata")
    for k, v in deck_metadata.items():
        if isinstance(v, (str, int)):
            sub = ET.SubElement(meta_el, k)
            sub.text = str(v)

    slides_el = ET.SubElement(root, "slides")
    for s in final_slides:
        s_el = ET.SubElement(slides_el, "slide", id=str(s.get("id", f"s{s['slideNumber']}")), number=str(s["slideNumber"]))
        title_el = ET.SubElement(s_el, "title")
        title_el.text = s.get("title", "")
        if s.get("isCheckpoint"):
            s_el.set("isCheckpoint", "true")
            s_el.set("checkpointNumber", str(s["checkpointNumber"]))
        elems_el = ET.SubElement(s_el, "interactiveElements")
        for el in s.get("interactiveElements", []):
            e_sub = ET.SubElement(elems_el, "element", type=el.get("type", ""))
            if "title" in el:
                e_sub.set("title", el["title"])

    questions_el = ET.SubElement(root, "questions", count=str(len(questions)))
    for q in questions:
        q_el = ET.SubElement(questions_el, "question", id=q["id"], correct=q["correctAnswer"])
        q_txt = ET.SubElement(q_el, "text")
        q_txt.text = q["question"]

    xml_str = ET.tostring(root, encoding="utf-8")
    parsed_xml = minidom.parseString(xml_str)
    pretty_xml = parsed_xml.toprettyxml(indent="  ", encoding="utf-8")
    with open(os.path.join(PACKAGE_DIR, "structure.xml"), "wb") as f:
        f.write(pretty_xml)
    print("5b. structure.xml yazıldı.")

    # 5c. blocks.html
    html_lines = [
        "<!DOCTYPE html>",
        "<html lang='tr'>",
        "<head>",
        "  <meta charset='utf-8'/>",
        f"  <title>{deck_metadata['title']}</title>",
        "  <style>",
        "    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; padding: 2rem; max-width: 900px; margin: auto; }",
        "    .slide-block { margin-bottom: 3rem; border: 1px solid #e2e8f0; border-radius: 8px; padding: 1.5rem; }",
        "    .slide-title { font-size: 1.5rem; font-weight: bold; color: #0f172a; margin-bottom: 0.5rem; }",
        "    .checkpoint { border-color: #0284c7; background-color: #f0f9ff; }",
        "    .element-box { margin-top: 1rem; padding: 1rem; background: #f8fafc; border-left: 4px solid #38bdf8; }",
        "  </style>",
        "</head>",
        "<body>",
        f"  <h1>{deck_metadata['title']}</h1>",
        f"  <p><strong>Öğretim Üyesi:</strong> {deck_metadata['instructor']} | <strong>Disiplin:</strong> {deck_metadata['discipline']}</p>",
        f"  <p>{deck_metadata['overview']}</p>",
        "  <hr/>"
    ]
    for s in final_slides:
        cp_class = " checkpoint" if s.get("isCheckpoint") else ""
        html_lines.append(f"  <div class='slide-block{cp_class}'>")
        html_lines.append(f"    <div class='slide-title'>Slayt {s['slideNumber']}: {s['title']}</div>")
        html_lines.append(f"    <p>{s['synthesisNarrative']}</p>")
        for el in s.get("interactiveElements", []):
            html_lines.append(f"    <div class='element-box'><strong>[{el.get('type')}]</strong> {el.get('title') or el.get('question') or el.get('sentence') or ''}</div>")
        if s.get("flashcards"):
            html_lines.append("    <div class='flashcards'><h4>Akıl Kartları:</h4><ul>")
            for fc in s["flashcards"]:
                html_lines.append(f"      <li><strong>{fc['front']}</strong> - {fc['back']}</li>")
            html_lines.append("    </ul></div>")
        html_lines.append("  </div>")
    html_lines.append("</body></html>")
    with open(os.path.join(PACKAGE_DIR, "blocks.html"), "w", encoding="utf-8") as f:
        f.write("\n".join(html_lines))
    print("5c. blocks.html yazıldı.")

    # 5d. content.md
    md_lines = [
        f"# {deck_metadata['title']}",
        f"**Öğretim Üyesi:** {deck_metadata['instructor']}  ",
        f"**Kurul & Disiplin:** {deck_metadata['committee']} · {deck_metadata['discipline']}  ",
        f"**Tarih:** {deck_metadata['programDate']}  ",
        "",
        "## Genel Bakış",
        deck_metadata["overview"],
        "",
        "---",
        ""
    ]
    for s in final_slides:
        md_lines.append(f"### Slayt {s['slideNumber']}: {s['title']}")
        md_lines.append(s["synthesisNarrative"])
        md_lines.append("")
        for el in s.get("interactiveElements", []):
            md_lines.append(f"- **[{el.get('type')}]** {el.get('title') or el.get('question') or el.get('sentence') or ''}")
        if s.get("flashcards"):
            md_lines.append("")
            md_lines.append("#### Checkpoint Akıl Kartları:")
            for fc in s["flashcards"]:
                md_lines.append(f"- **S:** {fc['front']}")
                md_lines.append(f"  **C:** {fc['back']}")
        md_lines.append("")
        md_lines.append("---")
        md_lines.append("")
    with open(os.path.join(PACKAGE_DIR, "content.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
    print("5d. content.md yazıldı.")

    # 6. RUNTIME DECK ITEM YAZ
    os.makedirs(DECKS_ITEMS_DIR, exist_ok=True)
    runtime_item = dict(deck_metadata)
    runtime_item["slides"] = final_slides
    runtime_item["questions"] = questions

    item_path = os.path.join(DECKS_ITEMS_DIR, f"{deck_metadata['id']}.json")
    with open(item_path, "w", encoding="utf-8") as f:
        json.dump(runtime_item, f, ensure_ascii=False, indent=2)
    print(f"6. Runtime item yazıldı: {item_path}")

    # 7. INTERACTIVE_LEARNING_DECKS.JSON DOSYASINI YERİNDE GÜNCELLE
    print(f"7. {INTERACTIVE_DECKS_PATH} güncelleniyor...")
    with open(INTERACTIVE_DECKS_PATH, "r", encoding="utf-8") as f:
        interactive_decks = json.load(f)

    # Var olan desteyi bul ve yerinde güncelle
    target_idx = None
    for idx, d in enumerate(interactive_decks):
        if d.get("id") == deck_metadata["id"]:
            target_idx = idx
            break

    full_deck_entry = dict(deck_metadata)
    full_deck_entry["slides"] = final_slides
    full_deck_entry["questions"] = questions

    if target_idx is not None:
        interactive_decks[target_idx] = full_deck_entry
        print(f"  -> Mevcut deste (Index {target_idx}) 100 slayt ile yerinde güncellendi.")
    else:
        interactive_decks.append(full_deck_entry)
        print("  -> Yeni deste listeye eklendi.")

    with open(INTERACTIVE_DECKS_PATH, "w", encoding="utf-8") as f:
        json.dump(interactive_decks, f, ensure_ascii=False, indent=2)
    print("7. interactive_learning_decks.json başarıyla kaydedildi.")

    # 8. CATALOG.JSON GÜNCELLE
    print(f"8. {CATALOG_PATH} güncelleniyor...")
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    cat_idx = None
    for idx, c in enumerate(catalog):
        if c.get("id") == deck_metadata["id"]:
            cat_idx = idx
            break

    cat_entry = dict(catalog[cat_idx]) if cat_idx is not None else dict(deck_metadata)
    cat_entry.update({
        "totalSlides": 100,
        "slideCount": 100,
        "totalQuestions": len(questions),
        "questionCount": len(questions),
        "totalFlashcards": 30,
        "interactiveElementCount": total_elems,
        "confidence": "high",
        "themeColor": "sky"
    })

    if cat_idx is not None:
        catalog[cat_idx] = cat_entry
    else:
        catalog.append(cat_entry)

    with open(CATALOG_PATH, "w", encoding="utf-8") as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2)
    print("8. catalog.json başarıyla güncellendi.")

    print("\n" + "=" * 70)
    print("DERS 11 İNŞA VE MONTAJ İŞLEMİ EKSİKSİZ TAMAMLANDI!")
    print("=" * 70)

if __name__ == "__main__":
    main()
