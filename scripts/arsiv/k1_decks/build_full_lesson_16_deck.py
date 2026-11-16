# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)
Master Deck Oluşturucu ve Çoklu Format Paketleyici.
100 Slayt, 10 Checkpoint (30 Akıl Kartı), 7 İnteraktif Eleman (%8+ Çeşitlilik),
Örnek Sorular, Runtime Item ve Multi-format Paketleme (manifest, structure, blocks, content).
"""

import os
import sys
import json
import re
import xml.etree.ElementTree as ET
from xml.dom import minidom
from collections import Counter

# Proje ana dizinini sys.path'e ekle
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from scripts.k1_16_deck_data.helpers import make_flashcard
from scripts.k1_16_deck_data.section_1 import get_section_1_slides
from scripts.k1_16_deck_data.section_2 import get_section_2_slides
from scripts.k1_16_deck_data.section_3 import get_section_3_slides
from scripts.k1_16_deck_data.section_4 import get_section_4_slides
from scripts.k1_16_deck_data.section_5 import get_section_5_slides
from scripts.k1_16_deck_data.section_6 import get_section_6_slides
from scripts.k1_16_deck_data.section_7 import get_section_7_slides
from scripts.k1_16_deck_data.section_8 import get_section_8_slides
from scripts.k1_16_deck_data.section_9 import get_section_9_slides
from scripts.k1_16_deck_data.section_10 import get_section_10_slides

from scripts.enrich_k1_16_elements import enrich_slides

# Dosya yolları
QUESTIONS_FILE = os.path.join(BASE_DIR, "meds/src/data/ornek_sorular/k1/k1-16-odem-hiperemi-konjesyon-ve-kanama.json")
PACKAGE_DIR = os.path.join(BASE_DIR, "meds/src/data/decks/packages/k1p-k1-16-odem-hiperemi-konjesyon-ve-kanama")
DECKS_ITEMS_DIR = os.path.join(BASE_DIR, "meds/src/data/decks/items")
INTERACTIVE_DECKS_PATH = os.path.join(BASE_DIR, "meds/src/data/interactive_learning_decks.json")
CATALOG_PATH = os.path.join(BASE_DIR, "meds/src/data/decks/catalog.json")

def fold(s):
    return str(s or '').lower().replace('ı', 'i').replace('İ', 'i')

def leaks(hint: str, answer: str) -> bool:
    """Exact leak check from validate_learning_decks.py"""
    if not hint or not answer:
        return False
    h = fold(hint)
    return any((w[:5] if len(w) > 5 else w) in h for w in re.findall(r'[\wçğıöşü%.,-]+', fold(answer)) if len(w) >= 3 or re.search(r'\d', w))

def sanitize_hint(hint: str, answer: str) -> str:
    if not hint or not leaks(hint, answer):
        return hint
    fallbacks = [
        "İlgili histopatolojik prensibi anımsayınız",
        "Ders notundaki hemodinamik kuralı düşününüz",
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
                "k1-16-fc-01",
                "Sağlıklı bir insanda toplam vücut suyunun kompartmanlara dağılım oranları nasıldır?",
                "Toplam vücut suyunun 2/3'ü hücre içinde (intrasellüler), 1/3'ü hücre dışındadır (ekstrasellüler: %80 interstisyel, %20 plazma).",
                "İki ana hacimsel oran ve alt dağılım", "Hemodinamik Denge"
            ),
            make_flashcard(
                "k1-16-fc-02",
                "Starling dengesinde sıvıyı damar dışına iten kuvvet ile damar içine geri çeken temel kuvvet hangileridir?",
                "İtici kuvvet kapiller hidrostatik basınç, geri çekici kuvvet ise plazma kolloid ozmotik (onkotik) basıncıdır.",
                "Zıt yönlü iki majör fiziksel vektör", "Hemodinamik Denge"
            ),
            make_flashcard(
                "k1-16-fc-03",
                "Plevral boşlukta sıvı birikmesine hidrotoraks, peritonda sıvıya asit denirken; tüm deri altı ve boşlukları tutan genel masif ödeme ne denir?",
                "Anasarkadır.",
                "Ağır yaygın sistemik ödem terimi", "Hemodinamik Denge"
            )
        ],
        19: [
            make_flashcard(
                "k1-16-fc-04",
                "Dokudaki kan hacmi artışını ifade eden süreçlerden hangisi aktif, hangisi pasif mekanizmayla gelişir?",
                "Hiperemi aktif arteriyoler dilatasyonla; konjesyon ise pasif venöz drenaj bozukluğuyla gelişir.",
                "Aktif ve pasif hemodinamik ikili", "Hiperemi ve Konjesyon"
            ),
            make_flashcard(
                "k1-16-fc-05",
                "Hiperemik dokunun parlak kırmızı ve sıcak, konjesyone dokunun ise siyanotik mavi ve soğuk olmasının nedeni nedir?",
                "Hiperemide oksihemoglobin zenginliği, konjesyonda ise venöz staz sonucu deoksihemoglobin birikimidir.",
                "İki farklı hemoglobin formu", "Hiperemi ve Konjesyon"
            ),
            make_flashcard(
                "k1-16-fc-06",
                "Kronik konjesyonda doku perfüzyonunun bozulması zamanla parankimde hangi kalıcı patolojik sonuçlara yol açar?",
                "Kronik hipoksi, parankim hücresi nekrozu, sekonder fibrozis ve kapiller rüptürüyle odaksal kanamalardır.",
                "Hipoksi ve bağ dokusu artış süreci", "Hiperemi ve Konjesyon"
            )
        ],
        29: [
            make_flashcard(
                "k1-16-fc-07",
                "Kronik sol kalp yetmezliğinde alveol lümeninde biriken hemosiderin yüklü alveoler makrofajlara verilen özel isim nedir?",
                "Kalp yetmezliği hücreleridir (siderofajlar).",
                "Pulmoner kronik konjesyonun hücresel göstergesi", "Organ Konjesyonu"
            ),
            make_flashcard(
                "k1-16-fc-08",
                "Kronik pulmoner konjesyonda septal fibrozis ve hemosiderin pigmenti birikimiyle akciğerin sert ve pas rengi almasına ne denir?",
                "Kahverengi endürasyondur (Brown induration).",
                "Sertleşme ve demir rengi tanımı", "Organ Konjesyonu"
            ),
            make_flashcard(
                "k1-16-fc-09",
                "Kronik sağ kalp yetmezliğinde karaciğer kesitinde lobül merkezi nekroze-kırmızı, perifer açık sarı-yağlı görünüme ne ad verilir?",
                "Muskat karaciğerdir (Nutmeg liver).",
                "Hint cevizi kesitine benzeyen alacalı manzara", "Organ Konjesyonu"
            )
        ],
        39: [
            make_flashcard(
                "k1-16-fc-10",
                "Konjestif kalp yetmezliğinde debi düşüşünü hipovolemi sanan böbreğin sodyum ve su tutarak ödemi derinleştirmesine ne denir?",
                "Sekonder hiperaldosteronizmdir (kardiyak kısır döngü).",
                "Böbrek aracılı sürrenal hormon uyarısı", "Hidrostatik Ödem"
            ),
            make_flashcard(
                "k1-16-fc-11",
                "Kardiyak ve hidrostatik ödemin yerçekimi etkisiyle ayakta bacaklarda, yatar pozisyonda presakral alanda toplanmasına ne denir?",
                "Bağımlı ödemdir (Dependent edema).",
                "Yerçekimine göre yer değiştiren sıvı dağılımı", "Hidrostatik Ödem"
            ),
            make_flashcard(
                "k1-16-fc-12",
                "Ödemli dokuya başparmakla bastırıldığında sıvının kenara itilmesiyle deride geçici bir çukur kalması özelliğine ne ad verilir?",
                "Gode bırakan ödemdir (Pitting edema).",
                "Parmak basısıyla çukurlaşan fizik muayene bulgusu", "Hidrostatik Ödem"
            )
        ],
        49: [
            make_flashcard(
                "k1-16-fc-13",
                "Plazma kolloid ozmotik (onkotik) basıncının yaklaşık %80'ini tek başına sağlayan majör plazma proteini nedir?",
                "Albümindir.",
                "Karaciğerde üretilen temel taşıyıcı protein", "Onkotik Basınç ve Hipoalbüminemi"
            ),
            make_flashcard(
                "k1-16-fc-14",
                "Günde 3.5 gram üzeri proteinüri, ağır hipoalbüminemi ve sabahları periorbital ödemle seyreden böbrek sendromu nedir?",
                "Nefrotik sendromdur.",
                "Masif albümin kaçağı sendromu", "Onkotik Basınç ve Hipoalbüminemi"
            ),
            make_flashcard(
                "k1-16-fc-15",
                "Karaciğer sirozlu bir hastada masif asit (karında sıvı birikimi) gelişmesini tetikleyen iki temel hemodinamik bozukluk nedir?",
                "Portal venöz hidrostatik basınç artışı (portal HT) ve albümin sentez yetersizliğidir (hipoalbüminemi).",
                "İkili Starling kuvvet dengesizliği", "Onkotik Basınç ve Hipoalbüminemi"
            )
        ],
        59: [
            make_flashcard(
                "k1-16-fc-16",
                "Kasık lenfatiklerini ve lenf nodlarını tıkayarak bacak ve genitalde masif elefantiyazise (fil hastalığı) yol açan parazit hangisidir?",
                "Wuchereria bancrofti parazitidir (filaryazis).",
                "Tropikal nematod etkeni", "Lenfatik ve Renal Ödem"
            ),
            make_flashcard(
                "k1-16-fc-17",
                "Meme kanserinde tümör hücrelerinin subdermal lenfatikleri tıkaması sonucu meme cildinde oluşan pürtüklü görünüme ne ad verilir?",
                "Peau d'orange (portakal kabuğu) manzarasıdır.",
                "Meme derisinde lenfödemik pürtüklenme", "Lenfatik ve Renal Ödem"
            ),
            make_flashcard(
                "k1-16-fc-18",
                "Akut poststreptokokal glomerülonefritte ödemin primer başlangıç mekanizması nedir?",
                "Glomerüler filtrasyon çöküşüne bağlı primer sodyum ve su retansiyonudur (hipervolemi).",
                "Böbreğin tuzu ve suyu süzüp atamaması", "Lenfatik ve Renal Ödem"
            )
        ],
        69: [
            make_flashcard(
                "k1-16-fc-19",
                "Kardiyojenik (hemodinamik) akut akciğer ödeminin klinik pratikteki en sık nedeni hangisidir?",
                "Sol ventrikül yetmezliğidir.",
                "Pulmoner venöz basıncı artıran sol kalp olayı", "Organa Özgü Ödem"
            ),
            make_flashcard(
                "k1-16-fc-20",
                "Akciğer ödeminde hava ile seröz transudanın çalkalanması sonucu bronşlardan dışarı sızan karakteristik sıvı nedir?",
                "Köpüklü pembe sıvıdır.",
                "Hava ile seröz sıvının fiziksel karışımı", "Organa Özgü Ödem"
            ),
            make_flashcard(
                "k1-16-fc-21",
                "Ağır serebral ödemde serebellar tonsillerin foramen magnumdan aşağı fıtıklaşarak beyin sapını ezmesi tablosuna ne ad verilir?",
                "Tonsiller herniasyondur.",
                "Solunum ve dolaşımı durduran en ölümcül fıtıklaşma", "Organa Özgü Ödem"
            )
        ],
        79: [
            make_flashcard(
                "k1-16-fc-22",
                "Damar duvarının tam kat mekanik yırtılmasıyla olan kanamaya ne ad verilir?",
                "Kanama per rhexindir (yırtılma/rüptür kanaması).",
                "Tam kat anatomik defekt kanaması", "Kanama ve Diyatezler"
            ),
            make_flashcard(
                "k1-16-fc-23",
                "C vitamini eksikliğinde (skorbüt) kapiller frajilite ve diş eti kanamalarının moleküler temeli nedir?",
                "Kollajen sentezinde prolin ve lizin aminoasitlerinin hidroksilasyon kusurudur.",
                "Kollajen çapraz bağ kurucu kofaktör eksikliği", "Kanama ve Diyatezler"
            ),
            make_flashcard(
                "k1-16-fc-24",
                "X'e bağlı resesif kalıtılan ve spontan eklem içi kanamalara (hemartroz) yol açan Faktör VIII eksikliği hastalığı nedir?",
                "Hemofili A'dır.",
                "Klasik faktör sekiz eksikliği koagülopatisi", "Kanama ve Diyatezler"
            )
        ],
        89: [
            make_flashcard(
                "k1-16-fc-25",
                "Deri, mukoza ve serözal yüzeylerdeki 1-2 mm çaplı noktasal kanamalara ne ad verilir?",
                "Peteşidir.",
                "1-2 mm çaplı punktat kanama odağı", "Kanama Tipleri ve Renk Döngüsü"
            ),
            make_flashcard(
                "k1-16-fc-26",
                "Deri muayenesinde 3-5 mm çapında lezyonların ele gelen kabarık (palpabl) purpura olması patognomonik olarak neyi gösterir?",
                "Lökositoklastik vasküliti (damar duvarı enflamasyonu ve nekrozu) gösterir.",
                "Damar yangısının deriyi kabartması", "Kanama Tipleri ve Renk Döngüsü"
            ),
            make_flashcard(
                "k1-16-fc-27",
                "Ekimozun enzimatik renk evriminde hemoglobin sırasıyla hangi iki ana pigment türevine ayrışır?",
                "Önce mavi-yeşil biliverdin/bilirubine, ardından altın-kahverengi hemosiderine dönüşür.",
                "İki ardışık yıkım pigmenti", "Kanama Tipleri ve Renk Döngüsü"
            )
        ],
        100: [
            make_flashcard(
                "k1-16-fc-28",
                "Sağlıklı bir yetişkinde ani gelişen kan kaybında fizyolojik kompensasyonla tolere edilebilen maksimum oran nedir?",
                "Toplam kan hacminin yaklaşık yüzde 20'sine (%20) kadar olan kayıptır.",
                "Kompansasyon eşiğini belirleyen kritik yüzde", "Klinik Entegrasyon"
            ),
            make_flashcard(
                "k1-16-fc-29",
                "Kronik dış kanamalar demir eksikliği anemisi yaparken, büyük iç hematomların demir eksikliği anemisi yapmamasının nedeni nedir?",
                "İç hematomdaki eritrositlerin doku makrofajlarınca parçalanarak demirin vücut içinde geri kazanılmasıdır (recycle).",
                "Demirin vücut içinde fagositozla kurtarılması", "Klinik Entegrasyon"
            ),
            make_flashcard(
                "k1-16-fc-30",
                "Perikard boşluğuna 150-250 ml kan dolması sonucu kalbin diyastolik genişlemesinin engellenmesi ve ani kardiyak arrest tablosuna ne ad verilir?",
                "Hemoperikardiyum ve kardiyak tamponaddır.",
                "Kalbin mekanik sıkışması tablosu", "Klinik Entegrasyon"
            )
        ]
    }

    # Her hint'i sanitize et
    sanitized_cards = {}
    for cp_idx, cards in raw_cards.items():
        clean_list = []
        for c in cards:
            c["hint"] = sanitize_hint(c.get("hint", ""), c.get("back", ""))
            clean_list.append(c)
        sanitized_cards[cp_idx] = clean_list

    return sanitized_cards

def build_lesson_16_deck():
    print("=" * 60)
    print("KURUL 1 - DERS 16: ÖDEM, HİPEREMİ, KONJESYON VE KANAMA")
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
            q_id = q.get("id") or f"k1-16-q{len(questions)+1:02d}"
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
    deck_id = "k1p-k1-16-odem-hiperemi-konjesyon-ve-kanama"
    deck_data = {
        "id": deck_id,
        "title": "Ödem, Hiperemi, Konjesyon ve Kanama",
        "description": "Hemodinamik homeostaz, Starling dengesi, sıvı kompartmanları, transuda vs eksuda, anasarka ve efüzyonlar, hiperemi (aktif) vs konjesyon (pasif), akut ve kronik akciğer konjesyonu ('kalp yetmezliği hücreleri' / siderofajlar, 'kahverengi endürasyon'), akut ve kronik karaciğer konjesyonu ('muskat karaciğeri', Zon 3 nekrozu, 'kardiyak siroz'), ödemin 5 temel mekanizması (hidrostatik basınç artışı, onkotik basınç azalması/hipoalbüminemi, lenfatik obstrüksiyon/lenfödem, primer ve sekonder sodyum/su retansiyonu, vasküler permeabilite artışı), kalp yetmezliği ve sekonder hiperaldosteronizm kısır döngüsü, bağımlı (dependent) ve gode bırakan (pitting) ödem, nefrotik sendrom ve sabah periorbital ödemi, karaciğer sirozu ve asit patofizyolojisi, lenfödem (peau d'orange, filaryazis/elefantiyazis, aksiller diseksiyon), organ ödemleri (akciğer ödemi ve pembe köpüklü balgam, beyin ödemi ve foramen magnum tonsiller herniasyonu), kanama (hemoraji) patolojisi (per rhexin vs per diapedesin), hemorajik diyatezler (vasküler frajilite/skorbüt, trombositopeni/ITP, trombositopati/Glanzmann/Bernard-Soulier/aspirin, koagülopati/hemofili A-B/K vitamini/siroz), kanama boyut sınıflaması (peteşi 1-2 mm, purpura 3-5 mm/vaskülit, ekimoz 1-2 cm/morarma, hematom, hemoperikardiyum ve kardiyak tamponad), ekimozun enzimatik renk döngüsü (hemoglobin -> bilirubin -> hemosiderin), %20 kan kaybı tolere edilme eşiği ve şok, lokalizasyon önemi (beyin sapı vs deri altı) ve dış kanama (demir eksikliği anemisi) vs iç hematom (demirin geri kazanımı ve sarılık) ayrımı.",
        "course": "Patoloji",
        "category": "Kurul 1 · 2026-2027 ders paketi",
        "instructor": "Prof. Dr. Hikmet Keleş (Patoloji ABD)",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "stepCount": len(enriched_slides),
        "questionCount": len(questions),
        "totalFlashcards": 30,
        "totalInteractiveElements": total_el,
        "slides": enriched_slides,
        "questions": questions
    }

    # 5. MULTI-FORMAT PAKETLEME (packages/k1p-k1-16-odem-hiperemi-konjesyon-ve-kanama)
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

    # 6. RUNTIME ITEM DOSYASI (items/k1p-k1-16-odem-hiperemi-konjesyon-ve-kanama.json)
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
                item["slideCount"] = deck_data["stepCount"]
                item["totalSlides"] = deck_data["stepCount"]
                item["cardCount"] = deck_data["totalFlashcards"]
                item["questionCount"] = deck_data["questionCount"]
                cat_updated = True
                print(f"8. catalog.json dizininde {deck_id} güncellendi.")
                break
        if cat_updated:
            with open(CATALOG_PATH, "w", encoding="utf-8") as f:
                json.dump(cat, f, ensure_ascii=False, indent=2)
            print(f"   {CATALOG_PATH} başarıyla kaydedildi.")

    print("\n" + "=" * 60)
    print("DERS 16 DESTE ÜRETİMİ VE ENTEGRASYONU TAMAMLANDI!")
    print("=" * 60)

if __name__ == "__main__":
    build_lesson_16_deck()
