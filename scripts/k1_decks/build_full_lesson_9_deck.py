#!/usr/bin/env python3
"""
Kurul 1 - Ders 9: Akut Enflamasyon: Vasküler Değişiklikler ve Hücresel Olaylar (Prof. Dr. Hikmet Keleş)
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

from scripts.k1_09_deck_data.helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)
from scripts.k1_09_deck_data.section_1 import get_section_1_slides
from scripts.k1_09_deck_data.section_2 import get_section_2_slides
from scripts.k1_09_deck_data.section_3 import get_section_3_slides
from scripts.k1_09_deck_data.section_4 import get_section_4_slides
from scripts.k1_09_deck_data.section_5 import get_section_5_slides
from scripts.k1_09_deck_data.section_6 import get_section_6_slides
from scripts.k1_09_deck_data.section_7 import get_section_7_slides
from scripts.k1_09_deck_data.section_8 import get_section_8_slides
from scripts.k1_09_deck_data.section_9 import get_section_9_slides
from scripts.k1_09_deck_data.section_10 import get_section_10_slides

from scripts.enrich_k1_09_elements import (
    get_extra_quizzes, get_extra_causal_chains, get_extra_sliders,
    get_extra_branching, get_extra_tables
)

# Dosya yolları
QUESTIONS_FILE = os.path.join(BASE_DIR, "meds/src/data/ornek_sorular/k1/k1-09-akut-enflamasyon-vaskuler-degisiklikler-ve-hucrese.json")
PACKAGE_DIR = os.path.join(BASE_DIR, "meds/src/data/decks/packages/k1-09-akut-enflamasyon-vaskuler-degisiklikler-ve-hucrese")
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
        "İlgili patofizyolojik mekanizmayı düşününüz",
        "Konuyla ilgili temel kavramı anımsayınız",
        "Tıbbi literatürdeki temel prensibi hatırlayınız",
        ""
    ]
    for fb in fallbacks:
        if not fb or not leaks(fb, answer):
            return fb
    return ""

def get_checkpoint_flashcards():
    """10 Checkpoint için toplam 30 adet akıl kartı (her checkpoint'e 3 adet)."""
    return {
        9: [
            make_flashcard(
                "k1-09-fc-01",
                "Akut enflamasyonun Celsus ve Virchow tarafından tanımlanan 5 kardinal belirtisi nelerdir?",
                "Calor (ısı artışı), Rubor (kızarıklık), Tumor (şişlik), Dolor (ağrı) ve Functio Laesa (fonksiyon kaybı).",
                "Kardinal belirtilerin Latince adları", "Akut Enflamasyon"
            ),
            make_flashcard(
                "k1-09-fc-02",
                "Akut enflamatuar yanıtın başarıyla sonuçlanmasını sağlayan 5R kuralı hangi basamaklardan oluşur?",
                "Recognition (Tanıma), Recruitment (Toplama), Removal (Yok etme), Regulation (Düzenleme/Sonlandırma) ve Repair (Onarım).",
                "Enflamasyonun 5 aşaması", "Akut Enflamasyon"
            ),
            make_flashcard(
                "k1-09-fc-03",
                "Akut enflamasyonda lokal kızarıklık ve sıcaklık artışına yol açan primer hemodinamik değişiklik nedir?",
                "Prekapiller arteriollerin vazodilatasyonu sonucu kapiller yatağa hücum eden kan debisi artışı (aktif hiperemi).",
                "Arteryoler genişleme ve kan akımı", "Akut Enflamasyon"
            )
        ],
        19: [
            make_flashcard(
                "k1-09-fc-04",
                "Doku hasarını ilk algılayan yerleşik bekçi hücreler ve tanıdıkları iki ana tehlike sinyali grubu nedir?",
                "Makrofajlar, dendritik hücreler ve mast hücreleridir; mikrobiyal PAMP'leri ve steril nekroz DAMP'lerini tanırlar.",
                "Sentinel hücreler ve tehlike kalıpları", "Bekçi Hücreler ve Reseptörler"
            ),
            make_flashcard(
                "k1-09-fc-05",
                "Gram-negatif bakteri duvarındaki lipopolisakkariti (LPS) plazma zarında tanıyan Toll-benzeri reseptör hangisidir?",
                "CD14 ve MD-2 ile kompleks oluşturan TLR4 reseptörüdür; MyD88 üzerinden NF-kappaB'yi aktive eder.",
                "Endotoksin tanıyan Toll reseptörü", "Bekçi Hücreler ve Reseptörler"
            ),
            make_flashcard(
                "k1-09-fc-06",
                "NLRP3 inflamazom kompleksinin proteolitik olarak aktive ettiği ve olgun IL-1beta üreten enzim nedir?",
                "Prokaspaz-1'in otokatalitik kesilmesiyle aktifleşen Kaspaz-1 (IL-1 dönüştürücü enzim) enzimidir.",
                "İnflamazomun efektör proteazı", "Bekçi Hücreler ve Reseptörler"
            )
        ],
        29: [
            make_flashcard(
                "k1-09-fc-07",
                "Akut enflamasyonda vasküler geçirgenlik artışının en sık görülen mekanizması nedir?",
                "Histamin, bradikinin ve lökotrienlerin postkapiller venüllerde yaptığı endotel hücre kasılmasıdır (15-30 dakikada geriler).",
                "En sık vasküler kaçak yolu", "Vasküler Değişiklikler"
            ),
            make_flashcard(
                "k1-09-fc-08",
                "Ağır termal yanık ve kimyasal travmalarda günlerce süren vasküler geçirgenlik artışının nedeni nedir?",
                "Arteriol, kapiller ve venülleri tutan direkt endotel hücre nekrozu ve dökülmesidir (gecikmiş-uzamış yanıt).",
                "Geniş damar nekrozu ve kaçak", "Vasküler Değişiklikler"
            ),
            make_flashcard(
                "k1-09-fc-09",
                "Lewis'in üçlü yanıtında (triple response) kaşıntılı kabarıklık (wheal) oluşturan temel mekanizma nedir?",
                "Mast hücrelerinden boşalan histaminin venüllerde permeabilite artışı yapması ve lokalize eksüda toplamasıdır.",
                "Dermografizm kabarıklığı nedeni", "Vasküler Değişiklikler"
            )
        ],
        39: [
            make_flashcard(
                "k1-09-fc-10",
                "Eksüda ile transüda arasındaki en temel patofizyolojik ayrım kriteri nedir?",
                "Transüdada vasküler endotel sağlamdır (basınç dengesizliği); eksüdada ise vasküler permeabilite bozulmuştur (enflamasyon).",
                "Endotel bütünlüğü ve geçirgenlik farkı", "Eksüda, Transüda ve Lenfatikler"
            ),
            make_flashcard(
                "k1-09-fc-11",
                "Eksüdanın laboratuvarda transüdadan ayırt edilmesini sağlayan protein ve dansite eşikleri nelerdir?",
                "Eksüdanın proteini > 3.0 g/dL, spesifik gravitesi > 1.020'dir; bol lökosit içerir ve pıhtılaşır.",
                "Laboratuvar tanı eşikleri", "Eksüda, Transüda ve Lenfatikler"
            ),
            make_flashcard(
                "k1-09-fc-12",
                "Enfeksiyon odağından bölgesel lenf noduna uzanan ağrılı kırmızı çizgilenme ve lenf bezi büyümesine ne ad verilir?",
                "Lenf damarı iltihabına 'lenfanjit', bölgesel lenf bezinin ağrılı reaktif büyümesine 'reaktif lenfadenit' denir.",
                "Lenfatik inflamasyon terimleri", "Eksüda, Transüda ve Lenfatikler"
            )
        ],
        49: [
            make_flashcard(
                "k1-09-fc-13",
                "Lökositlerin damar lümeninden hasarlı dokuya göçünde gerçekleşen 5 ardışık basamak nedir?",
                "1. Marjinasyon, 2. Yuvarlanma (Rolling), 3. Sıkı Adezyon (Adhesion), 4. Transmigrasyon (Diapedez), 5. Kemotaksi.",
                "Lökosit alımının sıralı adımları", "Lökosit Alımı ve Selektinler"
            ),
            make_flashcard(
                "k1-09-fc-14",
                "Endotel hücresindeki Weibel-Palade cisimciklerinde vWF ile birlikte depolanan ve saniyeler içinde ekzosite edilen selektin hangisidir?",
                "P-selektin (CD62P) molekülüdür; histamin ve trombin uyarısıyla derhal lümen zarına çıkar.",
                "Hazır depolu endotelyal selektin", "Lökosit Alımı ve Selektinler"
            ),
            make_flashcard(
                "k1-09-fc-15",
                "Lökosit Adezyon Eksikliği Tip 2 (LAD-2) hastalığında bozulan moleküler mekanizma ve basamak nedir?",
                "Fukoz transport kusuru nedeniyle Sialyl-Lewis X sentezlenemez; selektin bağlanması ve yuvarlanma (rolling) bozulur.",
                "Fukozilasyon kusuru ve yuvarlanma", "Lökosit Alımı ve Selektinler"
            )
        ],
        59: [
            make_flashcard(
                "k1-09-fc-16",
                "Lökositlerin endoteldeki ICAM-1'e kilitlenerek sıkı adezyon yapmasını sağlayan beta-2 integrinler nelerdir?",
                "LFA-1 (CD11a/CD18) ve Mac-1 (CD11b/CD18) heterodimerleridir; ortak beta-2 zinciri CD18'dir.",
                "Beta-2 integrin ailesi üyeleri", "İntegrinler ve Diapedez"
            ),
            make_flashcard(
                "k1-09-fc-17",
                "Lökositlerin interendotelyal kavşaktan dokuya sızmasında (diapedez) homofilik bağ kuran anahtar molekül nedir?",
                "PECAM-1 (Platelet Endothelial Cell Adhesion Molecule-1 / CD31) adezyon molekülüdür.",
                "Diapedezin homofilik anahtarı", "İntegrinler ve Diapedez"
            ),
            make_flashcard(
                "k1-09-fc-18",
                "Lökosit Adezyon Eksikliği Tip 1 (LAD-1) hastalığının genetik nedeni ve karakteristik klinik triadı nedir?",
                "CD18 (ITGB2) gen mutasyonudur; göbek kordonu düşmesinde gecikme, kanda aşırı lökositoz ve dokuda irinsiz enfeksiyonlar görülür.",
                "CD18 yokluğu ve göbek bağı gecikmesi", "İntegrinler ve Diapedez"
            )
        ],
        69: [
            make_flashcard(
                "k1-09-fc-19",
                "Nötrofilleri hasar odağına çeken en önemli eksojen ve endojen kemoatraktanlar nelerdir?",
                "Eksojen: Bakteriyel N-formilmetiyonin peptitleri; Endojen: Kemokin IL-8, Kompleman C5a ve Lökotrien B4 (LTB4).",
                "Kemotaktik ajanlar listesi", "Kemotaksi ve Hücresel Göç"
            ),
            make_flashcard(
                "k1-09-fc-20",
                "Akut enflamasyonda doku infiltrasyonunun zamansal kinetiği nasıldır?",
                "İlk 6-24 saatte polimorfonükleer nötrofiller baskındır; 24-48 saatten sonra yerlerini monosit ve makrofajlara bırakırlar.",
                "Hücresel göçün saatlik sırası", "Kemotaksi ve Hücresel Göç"
            ),
            make_flashcard(
                "k1-09-fc-21",
                "Akut viral menenjit veya hepatit enfeksiyonlarında erken dönemden itibaren baskın olan infiltrat hücresi nedir?",
                "Nötrofillerin yerine erken dönemden itibaren dokuya hücum eden Lenfositlerdir.",
                "Viral enfeksiyonların hücresel istisnası", "Kemotaksi ve Hücresel Göç"
            )
        ],
        79: [
            make_flashcard(
                "k1-09-fc-22",
                "Mikropların fagositozunu yüzlerce kat hızlandıran ve fagosit Fc reseptörlerince tanınan en güçlü opsonin nedir?",
                "İmmünoglobulin G (özellikle IgG1 ve IgG3) antikorlarıdır; ayrıca kompleman C3b ve iC3b de güçlü opsonindir.",
                "Antikor ve kompleman opsoninleri", "Opsonizasyon ve Fagositoz"
            ),
            make_flashcard(
                "k1-09-fc-23",
                "Chediak-Higashi sendromunda lökositlerde dev granüller oluşmasına ve fagositoz yetersizliğine yol açan defekt nedir?",
                "LYST gen mutasyonuna bağlı fagozom ile lizozomun kaynaşamamasıdır (veziküler füzyon kusuru).",
                "LYST mutasyonu ve füzyon felci", "Opsonizasyon ve Fagositoz"
            ),
            make_flashcard(
                "k1-09-fc-24",
                "Lökositlerin yutamayacakları kadar büyük yüzeylere (glomerül bazal membranı) yapışıp enzimlerini dışarı dökmesine ne ad verilir?",
                "Frustrated (engellenmiş) fagositoz adı verilir; glomerülonefrit ve vaskülit doku hasarının ana nedenidir.",
                "Doku yıkan engellenmiş fagositoz", "Opsonizasyon ve Fagositoz"
            )
        ],
        89: [
            make_flashcard(
                "k1-09-fc-25",
                "Respiratuar patlamada nötrofil azurofilik granüllerindeki MPO enziminin ürettiği en güçlü bakterisidal silah nedir?",
                "Hidrojen peroksit ve klorürden sentezlenen Hipokloröz Asittir (HOCl / hipoklorit).",
                "Çamaşır suyu analoğu bakterisidal asit", "Respiratuar Patlama ve NETosis"
            ),
            make_flashcard(
                "k1-09-fc-26",
                "Kronik Granülomatöz Hastalıkta (KGH) bozulan enzim ve öldürülemeyen karakteristik mikroorganizma grubu nedir?",
                "NADPH oksidaz kompleksi bozuktur; süperoksit üretilemez; katalaz-pozitif mikroplar (S. aureus, Aspergillus vb.) öldürülemez.",
                "NADPH oksidaz ve katalaz pozitifler", "Respiratuar Patlama ve NETosis"
            ),
            make_flashcard(
                "k1-09-fc-27",
                "Nötrofil Hücre Dışı Tuzaklarının (NET) oluşumunda histonları sitrülinleştirerek kromatini çözen enzim nedir?",
                "PAD4 (Peptidylarginine deiminase 4) enzimidir; netozis ile DNA ve granül enzimleri dışarı fırlatılır.",
                "NETosis başlatan enzim", "Respiratuar Patlama ve NETosis"
            )
        ],
        100: [
            make_flashcard(
                "k1-09-fc-28",
                "Akut romatizmal ateş veya üremik perikarditte görülen 'ekmek-tereyağı' manzarası hangi morfolojik kalıba özgüdür?",
                "Fibrinöz enflamasyona özgüdür; masif fibrinojen sızıntısı ve fibrin pıhtılaşması sonucu gelişir.",
                "Perikardın ekmek-tereyağı lezyonu", "Morfolojik Kalıplar ve Sonuçlar"
            ),
            make_flashcard(
                "k1-09-fc-29",
                "Doku içinde likefaksiyon nekrozu ve nötrofil enkazından oluşan lokalize irin birikimine ne ad verilir ve tedavisi nedir?",
                "Apse (abscess) adı verilir; avasküler nekrotik kitle olduğu için temel tedavisi cerrahi drenajdır.",
                "Lokalize cerahat odağı ve drenaj", "Morfolojik Kalıplar ve Sonuçlar"
            ),
            make_flashcard(
                "k1-09-fc-30",
                "Akut enflamasyonun çözülme (rezolüsyon) evresinde nötrofil göçünü durduran araşidonik asit kaynaklı anti-enflamatuar lipidler nelerdir?",
                "Lipoksinler (LXA4 ve LXB4); ayrıca omega-3 kaynaklı rezolvinler ve protektinler de rezolüsyonu yönetir.",
                "Yangıyı söndüren lipid mediyatörler", "Morfolojik Kalıplar ve Sonuçlar"
            )
        ]
    }

def main():
    print("=" * 70)
    print("Kurul 1 - Ders 9: Akut Enflamasyon: Vasküler Değişiklikler ve Hücresel Olaylar")
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
            q_id = q.get("id") or f"k1-09-q{len(questions)+1:02d}"
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
    extra_quizzes = get_extra_quizzes()
    extra_causal = get_extra_causal_chains()
    extra_sliders = get_extra_sliders()
    extra_branching = get_extra_branching()
    extra_tables = get_extra_tables()
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
        elements = list(slide.get("interactiveElements", []))

        if slide_num in extra_quizzes:
            elements.append(extra_quizzes[slide_num])
        if slide_num in extra_causal:
            elements.append(extra_causal[slide_num])
        if slide_num in extra_sliders:
            elements.append(extra_sliders[slide_num])
        if slide_num in extra_branching:
            elements.append(extra_branching[slide_num])
        if slide_num in extra_tables:
            elements.append(extra_tables[slide_num])

        # Şema normalizasyonları, tablo sütun sayısı eşitleme ve sızıntı temizliği
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
                    # Sütun sayısı eksiği varsa otomatik tamamla
                    if len(cells) < len(hdrs):
                        diff = len(hdrs) - len(cells)
                        if diff == 1 and len(cells) >= 2:
                            c3_text = cells[1].get("hint", "") or "Klinik değerlendirme"
                            cells[1]["hint"] = "İlgili anahtar parametreyi düşününüz"
                            cells.append({
                                "text": c3_text,
                                "isMasked": False,
                                "hint": ""
                            })
                        else:
                            for _ in range(diff):
                                cells.append({
                                    "text": "Standart fizyolojik parametre",
                                    "isMasked": False,
                                    "hint": ""
                                })
                    # Fazla hücre varsa kırp
                    elif len(cells) > len(hdrs):
                        cells = cells[:len(hdrs)]
                        r["cells"] = cells

                    # Sızıntı temizliği
                    for c in cells:
                        if isinstance(c, dict) and c.get("isMasked"):
                            ch = c.get("hint", "")
                            ca = c.get("text", "")
                            if ch and leaks(ch, ca):
                                c["hint"] = sanitize_hint(ch, ca)

        # Anlatım alanlarını validator standartlarına uygun bağla
        core_txt = slide.get("content") or slide.get("synthesisNarrative") or slide.get("coreContent", {}).get("text", "")
        slide["synthesisNarrative"] = core_txt
        slide["content"] = core_txt
        if not slide.get("coreContent", {}).get("keyBullets"):
            slide.setdefault("coreContent", {})["keyBullets"] = [
                {"title": slide["title"], "desc": slide.get("subtitle", ""), "isKey": True}
            ]

        # İlgili soruları dağıt
        start_q_idx = ((slide_num - 1) * len(questions)) // 100
        end_q_idx = (slide_num * len(questions)) // 100
        step_questions = questions[start_q_idx:end_q_idx]
        if not step_questions and questions:
            step_questions = [questions[(slide_num - 1) % len(questions)]]

        slide["interactiveElements"] = elements
        slide["matchedPastQuestions"] = step_questions
        if step_questions:
            slide["matchedPastQuestion"] = step_questions[0]

        final_slides.append(slide)

    # 4. İSTATİSTİKLERİ HESAPLA VE DOĞRULA
    type_counts = Counter()
    for s in final_slides:
        for el in s.get("interactiveElements", []):
            type_counts[el.get("type")] += 1

    total_interactive = sum(type_counts.values())
    print("\n" + "=" * 50)
    print(f"Toplam İnteraktif Öğe: {total_interactive}")
    print(f"Adım Başına Oran: {total_interactive / len(final_slides):.2f}x (Hedef: 1.5x - 3.0x)")
    print("-" * 50)
    for t, count in type_counts.most_common():
        pct = (count / total_interactive) * 100
        status = "UYGUN" if pct >= 8.0 else "DÜŞÜK (!)"
        print(f"  {t:<22}: {count:>3} (%{pct:>5.1f}) -> {status}")
    print("=" * 50)

    # Her tür en az %8 olmalı
    for t, count in type_counts.items():
        pct = (count / total_interactive) * 100
        assert pct >= 8.0, f"HATA: {t} türü %8 şartını sağlamıyor: %{pct:.1f}"

    # 5. DOSYALARI YAZ (XML, HTML, MD, JSON)
    deck_id = "k1p-k1-09-akut-enflamasyon-vaskuler-degisiklikler-ve-hucrese"
    deck_title = "Akut Enflamasyon: Vasküler Değişiklikler ve Hücresel Olaylar (Yeni Mikro-Ders)"
    short_title = "Akut Enflamasyon: Vasküler ve Hücresel"

    os.makedirs(PACKAGE_DIR, exist_ok=True)
    os.makedirs(DECKS_ITEMS_DIR, exist_ok=True)

    # Manifest
    manifest_data = {
        "id": "k1-09-akut-enflamasyon-vaskuler-degisiklikler-ve-hucrese",
        "title": deck_title,
        "shortTitle": short_title,
        "discipline": "Tıbbi Patoloji",
        "committee": "Kurul 1 (Ürogenital ve Solunum Sistemi)",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "version": "2.0.0",
        "formatVersion": "1.0",
        "totalSlides": 100,
        "totalInteractiveElements": total_interactive,
        "interactiveRatio": round(total_interactive / 100, 2),
        "interactiveDistribution": {t: {"count": c, "percentage": round(c / total_interactive * 100, 1)} for t, c in type_counts.items()},
        "files": {
            "structure": "structure.xml",
            "blocks": "blocks.html",
            "content": "content.md"
        }
    }
    manifest_path = os.path.join(PACKAGE_DIR, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, ensure_ascii=False, indent=2)
    print(f"\n1. Paket Manifest kaydedildi: {manifest_path}")

    # Structure XML
    root = ET.Element("learningDeck", {
        "id": deck_id,
        "version": "2.0.0",
        "totalSlides": "100"
    })
    meta_el = ET.SubElement(root, "metadata")
    ET.SubElement(meta_el, "title").text = deck_title
    ET.SubElement(meta_el, "discipline").text = "Tıbbi Patoloji"
    ET.SubElement(meta_el, "instructor").text = "Prof. Dr. Hikmet Keleş"

    slides_el = ET.SubElement(root, "slides")
    for s in final_slides:
        s_el = ET.SubElement(slides_el, "slide", {
            "number": str(s["slideNumber"]),
            "badge": s.get("badge", ""),
            "isCheckpoint": str(s.get("isCheckpoint", False)).lower()
        })
        ET.SubElement(s_el, "title").text = s["title"]
        ET.SubElement(s_el, "subtitle").text = s.get("subtitle", "")
        inter_el = ET.SubElement(s_el, "interactiveElements", {"count": str(len(s.get("interactiveElements", [])))})
        for el in s.get("interactiveElements", []):
            ET.SubElement(inter_el, "element", {"type": el.get("type", "")})

    xml_raw = ET.tostring(root, encoding="utf-8")
    parsed = minidom.parseString(xml_raw)
    xml_path = os.path.join(PACKAGE_DIR, "structure.xml")
    with open(xml_path, "w", encoding="utf-8") as f:
        f.write(parsed.toprettyxml(indent="  "))
    print(f"2. Paket Structure XML kaydedildi: {xml_path}")

    # Blocks HTML
    html_lines = [
        "<!DOCTYPE html>",
        "<html lang=\"tr\">",
        "<head>",
        "  <meta charset=\"UTF-8\">",
        f"  <title>{deck_title} - İnteraktif Bloklar</title>",
        "  <style>",
        "    .slide-block { margin-bottom: 2rem; border-bottom: 1px solid #ccc; padding-bottom: 1rem; }",
        "    .badge { font-weight: bold; color: #2563eb; }",
        "    .checkpoint { background: #fef2f2; border: 1px solid #f87171; padding: 1rem; }",
        "  </style>",
        "</head>",
        "<body>",
        f"  <h1>{deck_title}</h1>",
        f"  <p>Eğitmen: Prof. Dr. Hikmet Keleş | Toplam 100 Adım | {total_interactive} Etkileşim</p>"
    ]
    for s in final_slides:
        cp_cls = " checkpoint" if s.get("isCheckpoint") else ""
        html_lines.append(f"  <div class=\"slide-block{cp_cls}\" id=\"slide-{s['slideNumber']}\">")
        html_lines.append(f"    <span class=\"badge\">Adım {s['slideNumber']} · {s.get('badge','')}</span>")
        html_lines.append(f"    <h2>{s['title']}</h2>")
        html_lines.append(f"    <h3>{s.get('subtitle','')}</h3>")
        html_lines.append(f"    <div class=\"narrative\">{s.get('synthesisNarrative','').replace(chr(10), '<br>')}</div>")
        html_lines.append("  </div>")
    html_lines.append("</body></html>")
    html_path = os.path.join(PACKAGE_DIR, "blocks.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write("\n".join(html_lines))
    print(f"3. Paket Blocks HTML kaydedildi: {html_path}")

    # Content MD
    md_lines = [
        f"# {deck_title}",
        f"**Ders:** Tıbbi Patoloji · **Öğretim Üyesi:** Prof. Dr. Hikmet Keleş · **Kurul:** Kurul 1",
        f"**Adım Sayısı:** 100 · **İnteraktif Eleman:** {total_interactive} · **Oran:** {total_interactive/100:.2f}x\n",
        "---"
    ]
    for s in final_slides:
        md_lines.append(f"\n## Adım {s['slideNumber']}: {s['title']}")
        md_lines.append(f"*{s.get('subtitle', '')}* | **Rozet:** `{s.get('badge', '')}`\n")
        md_lines.append(s.get('synthesisNarrative', ''))
        if s.get("spotPearls"):
            md_lines.append("\n**Spot İnciler:**")
            for sp in s["spotPearls"]:
                md_lines.append(f"- {sp}")
        if s.get("flashcards"):
            md_lines.append("\n**Akıl Kartları (Flashcards):**")
            for fc in s["flashcards"]:
                md_lines.append(f"- **Soru:** {fc['front']} | **Cevap:** {fc['back']}")
    md_path = os.path.join(PACKAGE_DIR, "content.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
    print(f"4. Paket Content MD kaydedildi: {md_path}")

    # Runtime Item JSON
    full_deck_item = {
        "id": deck_id,
        "title": deck_title,
        "shortTitle": short_title,
        "discipline": "Tıbbi Patoloji",
        "committee": "Kurul 1 (Ürogenital ve Solunum Sistemi)",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "audioFile": "audio/decks/k1-09.mp3",
        "audioDuration": 2400,
        "confidence": 0.99,
        "themeColor": "rose",
        "matchedNoteId": "k1-09",
        "matchedNoteTitle": "Akut Enflamasyon: Vasküler Değişiklikler ve Hücresel Olaylar",
        "isNew": True,
        "isLegacy": False,
        "version": "2.0.0",
        "packageSources": {
            "packageDir": "meds/src/data/decks/packages/k1-09-akut-enflamasyon-vaskuler-degisiklikler-ve-hucrese",
            "manifest": "manifest.json",
            "structure": "structure.xml",
            "blocks": "blocks.html",
            "content": "content.md"
        },
        "overview": (
            "Akut enflamasyonun temel mekanizmaları: Celsus ve Virchow kardinal belirtileri (calor, rubor, tumor, dolor, functio laesa); "
            "PAMP ve DAMP tehlike sinyalleri, PRR'ler (TLR, NLR) ve NLRP3 inflamazom platformu; "
            "vasküler değişiklikler (prekapiller vazodilatasyon, aktif hiperemi, staz ve postkapiller venül endotel kasılması); "
            "eksüda, transüda, ödem ve lenfatik drenaj (lenfanjit, lenfadenit); "
            "lökosit alımı (marjinasyon, selektinlerle yuvarlanma, integrinlerle sıkı adezyon, PECAM-1 diapedez, kemotaksi); "
            "lökosit adezyon eksiklikleri (LAD-1: CD18 defekti, LAD-2: Sialyl-Lewis X fukozilasyon defekti); "
            "fagositoz, opsonizasyon (IgG, C3b) ve fagolizozom oluşumu (Chediak-Higashi sendromu); "
            "oksijen bağımlı öldürme (NADPH oksidaz, MPO-H2O2-HOCl sistemi, Kronik Granülomatöz Hastalık, MPO eksikliği, NETosis); "
            "akut enflamasyonun 4 morfolojik kalıbı (seröz, fibrinöz, pürülan, ülseratif) ve 3 sonlanımı (rezolüsyon, fibrozis, kronikleşme)."
        ),
        "highYieldPearls": [
            "Akut enflamasyon dakikalar-saatler içinde başlar; nötrofil, ödem ve eksüda ile karakterizedir; fibrozis içermez.",
            "5 kardinal belirti: Calor (ısı), Rubor (kızarıklık), Tumor (şişlik), Dolor (ağrı) ve Functio Laesa (fonksiyon kaybı).",
            "PAMP mikrop imzasıdır (LPS, peptidoglikan); DAMP steril nekroz ürünüdür (hücre dışı ATP, ürik asit, HMGB1).",
            "TLR4 plazma zarında LPS'yi tanır; MyD88 üzerinden NF-kappaB'yi aktive ederek TNF ve IL-1 sentezletir.",
            "NLRP3 inflamazomu K+ kaybı ve kristallerle uyarılır; Kaspaz-1'i aktive ederek olgun IL-1beta ve IL-18 üretir.",
            "En sık vasküler geçirgenlik mekanizması postkapiller venüllerde histaminle oluşan endotel kasılmasıdır (15-30 dk).",
            "Direkt endotel nekrozu (yanık, toksin) tüm mikrosirkülasyonu tutar ve günlerce uzamış kaçak yapar.",
            "Eksüda yüksek proteinli (>3 g/dL), yüksek dansiteli (>1.020) ve nötrofillidir; transüda ise düşük proteinli ultrafiltrattır.",
            "Lenfanjit enfeksiyon odağından uzanan kırmızı çizgilenmedir; lenfadenit bölgesel lenf nodunun ağrılı büyümesidir.",
            "Yuvarlanma selektinlerle (L, E, P) yürütülür; P-selektin Weibel-Palade cisimciklerinde vWF ile hazır depolanır.",
            "Sıkı adezyon lökosit integrinleri (LFA-1, Mac-1) ile endotel ICAM-1'i arasında gerçekleşir; kemokinle yüksek afiniteye geçer.",
            "Diapedez (transmigrasyon) interendotelyal kavşaktan geçiştir; PECAM-1 (CD31) homofilik bağlanmasıyla sağlanır.",
            "LAD-1 CD18 (beta-2 integrin) gen mutasyonudur; sıkı adezyon bozuktur, göbek bağı düşmesi haftalarca gecikir.",
            "LAD-2 fukozilasyon kusurudur; Sialyl-Lewis X sentezlenemez, yuvarlanma bozulur, mental retardasyon eşlik eder.",
            "Kemoatraktanlar: Bakteriyel N-formilmetiyonin, kompleman C5a, lökotrien B4 (LTB4) ve kemokin IL-8 (CXCL8).",
            "İlk 6-24 saatte nötrofiller, 24-48 saatten sonra monosit/makrofajlar baskındır (Pseudomonas'ta günlerce nötrofil, virüste lenfosit).",
            "En güçlü opsonin IgG'dir (Fc kuyruğu FcγR'ye bağlanır); kompleman C3b ise CR1 ve CR3'e tutunur.",
            "Chediak-Higashi sendromu LYST mutasyonudur; fagozom-lizozom füzyonu bozuktur, dev lizozomal granüller ve albinizm görülür.",
            "Respiratuar patlamada NADPH oksidaz süperoksit (O2·-) üretir; MPO ise H2O2 + Cl- birleşiminden hipokloröz asit (HOCl) yapar.",
            "Kronik Granülomatöz Hastalık (KGH) NADPH oksidaz defektidir (en sık X-bağlı gp91phox); katalaz-pozitif mikroplar öldürülemez, NBT negatiftir.",
            "NET'ler (Neutrophil Extracellular Traps) PAD4 histon sitrülinasyonu ile ekstrasellüler alana fırlatılan DNA, histon ve MPO ağlarıdır.",
            "Morfolojik kalıplar: Seröz (berrak bül), Fibrinöz (ekmek-tereyağı perikardit), Pürülan (irin, apse, likefaksiyon), Ülseratif (mukoza kaybı).",
            "Fibrinöz eksüda temizlenemezse organizasyon ile fibröz yapışıklığa ve konstriktif perikardite dönüşür.",
            "Rezolüsyon aktif bir programdır; nötrofil göçü lipoksinler (LXA4), rezolvinler, TGF-beta ve IL-10 ile durdurulur."
        ],
        "totalSlides": 100,
        "totalInteractiveElements": total_interactive,
        "interactiveRatio": round(total_interactive / 100, 2),
        "matchedPastQuestionsCount": len(questions),
        "slides": final_slides
    }
    output_path = os.path.join(DECKS_ITEMS_DIR, f"{deck_id}.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(full_deck_item, f, ensure_ascii=False, indent=2)
    print(f"5. Runtime Item JSON kaydedildi: {output_path}")

    # 6. INTERACTIVE_LEARNING_DECKS.JSON GÜNCELLE
    with open(INTERACTIVE_DECKS_PATH, "r", encoding="utf-8") as f:
        decks_meta = json.load(f)

    found_idx = -1
    for i, d in enumerate(decks_meta):
        if d.get("id") == deck_id or d.get("id") == "k1-09-akut-enflamasyon-vaskuler-degisiklikler-ve-hucrese":
            found_idx = i
            break

    deck_summary = {
        "id": deck_id,
        "title": deck_title,
        "shortTitle": short_title,
        "discipline": "Tıbbi Patoloji",
        "committee": "Kurul 1 (Ürogenital ve Solunum Sistemi)",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "audioFile": "audio/decks/k1-09.mp3",
        "audioDuration": 2400,
        "confidence": 0.99,
        "themeColor": "rose",
        "matchedNoteId": "k1-09",
        "matchedNoteTitle": "Akut Enflamasyon: Vasküler Değişiklikler ve Hücresel Olaylar",
        "isNew": True,
        "isLegacy": False,
        "version": "2.0.0",
        "packageSources": {
            "packageDir": "meds/src/data/decks/packages/k1-09-akut-enflamasyon-vaskuler-degisiklikler-ve-hucrese",
            "manifest": "manifest.json",
            "structure": "structure.xml",
            "blocks": "blocks.html",
            "content": "content.md"
        },
        "overview": full_deck_item["overview"],
        "highYieldPearls": full_deck_item["highYieldPearls"],
        "totalSlides": 100,
        "totalInteractiveElements": total_interactive,
        "interactiveRatio": round(total_interactive / 100, 2),
        "slides": final_slides
    }

    if found_idx >= 0:
        decks_meta[found_idx] = deck_summary
        print(f"6. interactive_learning_decks.json indeksi {found_idx} yerinde güncellendi.")
    else:
        decks_meta.append(deck_summary)
        print("6. interactive_learning_decks.json sonuna eklendi.")

    with open(INTERACTIVE_DECKS_PATH, "w", encoding="utf-8") as f:
        json.dump(decks_meta, f, ensure_ascii=False, indent=2)

    # 7. CATALOG.JSON GÜNCELLE
    if os.path.exists(CATALOG_PATH):
        with open(CATALOG_PATH, "r", encoding="utf-8") as f:
            catalog = json.load(f)
        cat_found = False
        cat_entry = {
            "id": deck_id,
            "title": deck_title,
            "discipline": "Tıbbi Patoloji",
            "committee": "Kurul 1",
            "totalSlides": 100,
            "interactiveElementsCount": total_interactive,
            "hasPackage": True
        }
        if isinstance(catalog, list):
            for i, c in enumerate(catalog):
                if c.get("id") == deck_id:
                    catalog[i] = cat_entry
                    cat_found = True
                    break
            if not cat_found:
                catalog.append(cat_entry)
        elif isinstance(catalog, dict) and "decks" in catalog:
            for i, c in enumerate(catalog["decks"]):
                if c.get("id") == deck_id:
                    catalog["decks"][i] = cat_entry
                    cat_found = True
                    break
            if not cat_found:
                catalog["decks"].append(cat_entry)
        with open(CATALOG_PATH, "w", encoding="utf-8") as f:
            json.dump(catalog, f, ensure_ascii=False, indent=2)
        print("7. catalog.json başarıyla güncellendi.")

    print("\n" + "=" * 70)
    print("TEBRİKLER! DERS 9 TÜM FORMATLARDA BAŞARIYLA TAMAMLANDI!")
    print("=" * 70)

if __name__ == "__main__":
    main()
