# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 19: Doğumsal Kadın/Erkek Genital Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)
Master Deck Oluşturucu ve Multi-Format Paketleyici.
- 10 Bölüm, 100 Slayt, 10 Checkpoint (her birinde 3 akıl kartı -> toplam 30 akıl kartı).
- 7 İnteraktif Eleman Tipi (her biri en az %8.0 çeşitlilikte).
- Multi-format paketleme: manifest.json, structure.xml, blocks.html, content.md.
- Runtime item: meds/src/data/decks/items/k1p-k1-19-dogumsal-kadin-erkek-genital-gelisim-anomalileri.json
- Yerinde güncelleme: meds/src/data/interactive_learning_decks.json (İndeks 66) ve catalog.json.
"""

import os
import sys
import json
import re
from collections import Counter
import xml.etree.ElementTree as ET
from xml.dom import minidom

# Proje ana dizinini sys.path'e ekle
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from scripts.k1_19_deck_data.helpers import make_flashcard
from scripts.k1_19_deck_data.section_1 import get_section_1_slides
from scripts.k1_19_deck_data.section_2 import get_section_2_slides
from scripts.k1_19_deck_data.section_3 import get_section_3_slides
from scripts.k1_19_deck_data.section_4 import get_section_4_slides
from scripts.k1_19_deck_data.section_5 import get_section_5_slides
from scripts.k1_19_deck_data.section_6 import get_section_6_slides
from scripts.k1_19_deck_data.section_7 import get_section_7_slides
from scripts.k1_19_deck_data.section_8 import get_section_8_slides
from scripts.k1_19_deck_data.section_9 import get_section_9_slides
from scripts.k1_19_deck_data.section_10 import get_section_10_slides
from scripts.enrich_k1_19_elements import apply_enrichment

QUESTIONS_FILE = os.path.join(PROJECT_ROOT, "meds/src/data/ornek_sorular/k1/k1-19-dogumsal-kadin-erkek-genital-gelisim-anomalileri.json")
PACKAGE_DIR = os.path.join(PROJECT_ROOT, "meds/src/data/decks/packages/k1p-k1-19-dogumsal-kadin-erkek-genital-gelisim-anomalileri")
DECKS_ITEMS_DIR = os.path.join(PROJECT_ROOT, "meds/src/data/decks/items")
INTERACTIVE_DECKS_PATH = os.path.join(PROJECT_ROOT, "meds/src/data/interactive_learning_decks.json")
CATALOG_PATH = os.path.join(PROJECT_ROOT, "meds/src/data/decks/catalog.json")

def leaks(hint: str, answer: str) -> bool:
    """İpucu ile cevap arasındaki sızıntıyı kontrol eder."""
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

def get_checkpoint_flashcards():
    """10 Checkpoint için toplam 30 adet akıl kartı (her checkpoint'e 3 adet)."""
    raw_cards = {
        9: [
            make_flashcard(
                "k1-19-fc-01",
                "İnsan fertilizasyonunun embriyolojik gelişimdeki üç temel biyolojik görevi nedir?",
                "Diploid 46 kromozomu tamamlamak, genetik cinsiyeti belirlemek ve embriyogenezi başlatmak.",
                "Zigot oluşumuyla sağlanan temel gelişimsel adımlar", "Fertilizasyon"
            ),
            make_flashcard(
                "k1-19-fc-02",
                "Fertilizasyondan sonra oluşan blastosistin endometriyuma implante olduğu ve maternal kanda hCG'nin pozitifleştiği post-konsepsiyonel gün hangisidir?",
                "6. gündür (Altıncı gün).",
                "Uterusa gömülmenin gerçekleştiği embriyonik takvim zamanı", "Erken Gelişim"
            ),
            make_flashcard(
                "k1-19-fc-03",
                "Alfred Jost'un 1947 yılındaki tavşan embriyosu deneyine göre gonadal hormonların yokluğunda memeli genital sistemi hangi varsayılan yönde gelişir?",
                "Dişi yönünde gelişir (Dişi varsayılan fenotiptir).",
                "Gonad çıkarıldığında embriyonun otomatik izlediği anatomik yön", "Embriyoloji Prensipleri"
            )
        ],
        19: [
            make_flashcard(
                "k1-19-fc-04",
                "Y kromozomunun kısa kolunda bulunan SRY geni embriyogenezin kaçıncı gününde presertoli hücrelerinde en yüksek ekspresyon düzeyine (pik) ulaşır?",
                "41. günde (Kırk birinci gün).",
                "Presertoli hücrelerinde tepe noktasına çıkan embriyonik takvim zamanı", "Testis Genetiği"
            ),
            make_flashcard(
                "k1-19-fc-05",
                "17q24 lokusundaki heterozigot fonksiyon kaybı mutasyonu uzun kemiklerde eğrilik (Kampomelik Displazi) ile 46,XY cinsiyet tersinmesine yol açan otozomal gen hangisidir?",
                "SOX9 genidir.",
                "Otozomal testis belirleyici ana transkripsiyon faktörü", "Testis Genetiği"
            ),
            make_flashcard(
                "k1-19-fc-06",
                "Ekzon 8-9 missense mutasyonunda Denys-Drash (Wilms tümörü), intron 9 splice mutasyonunda Frasier sendromu yapan 11p13 lokusundaki gen hangisidir?",
                "WT1 (Wilms Tumor 1) genidir.",
                "Böbrek ve katlantı taslağını kuran çinko parmaklı lokus", "Gonadal Disgenezi"
            )
        ],
        29: [
            make_flashcard(
                "k1-19-fc-07",
                "Over belirleyici WNT4 geninin homozigot kaybı sonucu 46,XX cinsiyet tersinmesi, böbrek agenezisi ve adrenal disgenezisi ile giden letal sendrom hangisidir?",
                "SERKAL sendromudur.",
                "WNT4 tam yokluğunda görülen çoklu organ displazisi", "Over Genetiği"
            ),
            make_flashcard(
                "k1-19-fc-08",
                "Postnatal dönemde over granüloza hücre kimliğini koruyan ve mutasyonunda blefarofimozis ile prematür over yetmezliği (BPES) görülen 3q23 lokusundaki gen hangisidir?",
                "FOXL2 genidir.",
                "Göz kapağı anomalisi ve erken menopozla ilişkili faktör", "Over Genetiği"
            ),
            make_flashcard(
                "k1-19-fc-09",
                "Xp21 bölgesindeki duplikasyonunda 46,XY dişi fenotip, inaktive edici mutasyonunda ise X'e bağlı adrenal hipoplazi yapan nükleer represör gen hangisidir?",
                "DAX1 (NR0B1) genidir.",
                "Dozaj duyarlı cinsiyet tersinmesi bölgesindeki X faktörü", "Cinsiyet Tersinmesi"
            )
        ],
        39: [
            make_flashcard(
                "k1-19-fc-10",
                "Fetal yaşamın 8-10. haftalarında testis Sertoli hücrelerinden salgılanarak paramezonefrik Müller kanallarının gerilemesini sağlayan hormon hangisidir?",
                "AMH (Anti-Müllerian Hormon / MIS).",
                "TGF-beta ailesinden olan kanal eritici glikoprotein", "Kanal Sistemleri"
            ),
            make_flashcard(
                "k1-19-fc-11",
                "Hedef dış genital dokularda 5α-redüktaz 2 enzimi tarafından üretilerek genital tüberkülün penise, katlantıların skrotuma dönüşmesini sağlayan yüksek afiniteli androjen hangisidir?",
                "Dihidrotestosterondur (DHT).",
                "Erkek dış genitalyasının primer maskülinizan molekülü", "Dış Genitalya"
            ),
            make_flashcard(
                "k1-19-fc-12",
                "Testislerin intraabdominal bölgeden inguinal halkaya inişini (transabdominal faz) gubernakulumdaki RXFP2 reseptörüne bağlanarak yöneten Leydig hormonu hangisidir?",
                "INSL3 (İnsülin benzeri peptid 3 / RLF).",
                "Gubernakulumu kalınlaştırıp ilk desensusu sağlayan insülinomimetik faktör", "Testis İnişi"
            )
        ],
        49: [
            make_flashcard(
                "k1-19-fc-13",
                "2006 Chicago Konsensüsü sınıflamasına göre eski 'gerçek hermafroditizm' teriminin modern tıptaki tam bilimsel karşılığı nedir?",
                "Ovotestiküler CGB'dir.",
                "Aynı bireyde folikül ve seminifer tübül bulunması durumu", "CGB Sınıflaması"
            ),
            make_flashcard(
                "k1-19-fc-14",
                "Ovotestiküler CGB olgularında en sık (%60-70) saptanan kromozomal karyotip hangisidir?",
                "46,XX karyotipidir.",
                "Olguların üçte ikisinde saptanan genetik formül", "Ovotestiküler CGB"
            ),
            make_flashcard(
                "k1-19-fc-15",
                "Prader sınıflamasına göre büyümüş klitoris ile birlikte vajina ve üretranın birleşerek tek bir ortak ürogenital sinüse açıldığı evre kaçtır?",
                "Prader Evre 3'tür.",
                "Tek orifisli ortak kavitenin belirleyici olduğu basamak derecesi", "Prader Evrelemesi"
            )
        ],
        59: [
            make_flashcard(
                "k1-19-fc-16",
                "47,XXY Klinefelter sendromlu bir erkeğinInterfaz çekirdeklerinde Lyon hipotezine göre kaç adet Barr cisimciği gözlenir?",
                "1 adettir (Bir adet).",
                "X kromozomu sayısından tek eksiltilerek hesaplanan heterokromatin", "Kromozom Anomalileri"
            ),
            make_flashcard(
                "k1-19-fc-17",
                "45,X Turner sendromlu hastalarda görülen orantısız boy kısalığından sorumlu olan psödootozomal bölge (PAR1) geni hangisidir?",
                "SHOX genidir.",
                "Büyüme plaklarını yöneten homeobox ailesi üyesi", "Turner Sendromu"
            ),
            make_flashcard(
                "k1-19-fc-18",
                "Bir tarafında disgenetik testis, diğer tarafında streak gonad bulunan ve gonadoblastom riski taşıyan asimetrik mozaik karyotip hangisidir?",
                "45,X/46,XY mozaik karyotipidir (Miks Gonadal Disgenezi).",
                "Bir yanda atipik organ diğer yanda fibröz bant taşıyan asimetrik hücresel durum", "Gonadal Disgenezi"
            )
        ],
        69: [
            make_flashcard(
                "k1-19-fc-19",
                "5α-redüktaz tip 2 eksikliğine yol açan, 2p23 lokusunda kodlanan ve otozomal resesif kalıtılan gen hangisidir?",
                "SRD5A2 genidir.",
                "Dış üreme dokularında androjen metabolitini üreten 2p23 lokusundaki kalıtım lokusu", "5α-Redüktaz"
            ),
            make_flashcard(
                "k1-19-fc-20",
                "5α-redüktaz 2 eksikliği tanısında hCG stimülasyonu sonrasında serum Testosteron / Dihidrotestosteron (T/DHT) oranının kaçın üzerinde olması patognomoniktir?",
                "30'un üzerindedir (>30).",
                "Enzimatik dönüşüm bloğunu kanıtlayan biyokimyasal oran eşiği", "5α-Redüktaz Tanı"
            ),
            make_flashcard(
                "k1-19-fc-21",
                "Doğumda kız yetiştirilen 5α-redüktaz eksikliği olgularında pubertede penis büyümesi, ses kalınlaşması ve testis inişini sağlayan temel hormonal olay nedir?",
                "Testis kaynaklı aşırı testosteron patlaması ve tip 1 enzimin devreye girmesidir.",
                "Ergenlikte gerçekleşen dramatik androjen dalgası", "Pubertal Virilizasyon"
            )
        ],
        79: [
            make_flashcard(
                "k1-19-fc-22",
                "Komplet Androjen Duyarsızlık Sendromuna (CAIS) yol açan ve Xq11-12 lokusunda yer alan nükleer reseptör geni hangisidir?",
                "AR (Androjen Reseptörü) genidir.",
                "Xq11-12 lokusunda yer alan nükleer protein faktörü", "Androjen Duyarsızlığı"
            ),
            make_flashcard(
                "k1-19-fc-23",
                "Komplet Androjen Duyarsızlık Sendromunda (CAIS) dış fenotip tam dişi olmasına rağmen pelviste neden uterus ve fallop tüpleri bulunmaz?",
                "Testis Sertoli hücrelerinin normal AMH salgılaması nedeniyle.",
                "Müller kanallarını eriten glikoproteinin varlığı", "CAIS Anatomisi"
            ),
            make_flashcard(
                "k1-19-fc-24",
                "CAIS hastalarında intraabdominal testislerin cerrahi olarak çıkarılmasının (gonadektomi) puberte sonrasına ertelenmesinin gerekçesi nedir?",
                "Aromataz aracılığıyla doğal meme ve kemik gelişiminin kendi hormonlarıyla tamamlanmasını sağlamak.",
                "Endojen östrojen kaynağı ile sekonder kadın özelliklerinin olgunlaşmasını beklemek", "CAIS Yönetimi"
            )
        ],
        89: [
            make_flashcard(
                "k1-19-fc-25",
                "46,XX kuşkulu genitalya olgularının en sık nedeni olan ve KAH vakalarının %90-95'ini oluşturan enzim eksikliği hangisidir?",
                "21-Hidroksilaz (CYP21A2) eksikliğidir.",
                "Kortizol ve aldosteron yapımında progesteron basamağını katalizleyen mikrozomal enzim", "KAH Etiyolojisi"
            ),
            make_flashcard(
                "k1-19-fc-26",
                "21-hidroksilaz eksikliğinde enzim bloğunun önünde biriken ve yenidoğan topuk kanı taramasında bakılan temel steroid belirteci nedir?",
                "17-Hidroksiprogesterondur (17-OHP).",
                "Guthrie kağıdında ölçülen KAH tarama parametresi", "KAH Tarama"
            ),
            make_flashcard(
                "k1-19-fc-27",
                "Klasik KAH'ın tuz kaybettirici formunda doğumdan sonraki 1-2. haftalarda görülen hayatı tehdit edici tipik serum elektrolit tablosu nasıldır?",
                "Hiponatremi ve hiperkalemidir.",
                "Düşük sodyum ve yüksek potasyum ile giden kriz tablosu", "Adrenal Kriz"
            )
        ],
        100: [
            make_flashcard(
                "k1-19-fc-28",
                "KAH riskli gebeliklerde kız fetusun virilize olmasını önlemek amacıyla anneye en geç 6-8. haftada başlanan plasentayı geçen ilaç hangisidir?",
                "Deksametazondur.",
                "11β-HSD2 tarafından yıkılmadan fetusa ulaşan sentetik steroid", "Prenatal Tedavi"
            ),
            make_flashcard(
                "k1-19-fc-29",
                "Prenatal deksametazon tedavisinde CVS sonucunda fetus 46,XY erkek veya sağlıklı kız çıktığında yapılması gereken klinik karar nedir?",
                "Deksametazon tedavisi derhal kesilmelidir.",
                "Fetusu gereksiz steroid maruziyetinden koruma prensibi", "Prenatal Yönetim"
            ),
            make_flashcard(
                "k1-19-fc-30",
                "Kuşkulu genitalya ile doğan bir yenidoğanda bilateral gonadların palpe edilememesi durumunda ilk dışlanması gereken hayatı tehdit edici durum nedir?",
                "46,XX Konjenital Adrenal Hiperplazidir (Tuz kaybettirici kriz riski).",
                "Bilateral non-palpabl gonadda acil araştırılan ölümcül böbrek üstü bezi steroidogenez acili", "Tanı Algoritması"
            )
        ]
    }
    return raw_cards

def build_lesson_19_deck():
    print("=" * 60)
    print("KURUL 1 - DERS 19: DOĞUMSAL KADIN/ERKEK GENİTAL GELİŞİM ANOMALİLERİ")
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
            q_id = q.get("id") or f"k1-19-q{len(questions)+1:02d}"
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

    # 3. İNTERAKTİF ELEMAN ÇEŞİTLİLİĞİNİ DENGELE (%8+ KURALI)
    slides = apply_enrichment(raw_slides)
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
    checkpoint_cards = get_checkpoint_flashcards()
    all_flashcards = []
    checkpoint_indices = [9, 19, 29, 39, 49, 59, 69, 79, 89, 100]

    for cp_num in checkpoint_indices:
        slide_idx = cp_num - 1
        s = slides[slide_idx]
        cards = checkpoint_cards.get(cp_num, [])
        assert len(cards) == 3, f"HATA: Slayt {cp_num} için 3 akıl kartı olmalı, {len(cards)} var!"
        s["flashcards"] = cards
        all_flashcards.extend(cards)

    print(f"4. 10 Checkpoint'e toplam {len(all_flashcards)} akıl kartı eklendi (Her checkpoint'te 3 adet).")

    # Hint sızıntısı kontrolü
    leak_count = 0
    for fc in all_flashcards:
        if leaks(fc.get("hint", ""), fc.get("back", "")):
            leak_count += 1
            print(f"   UYARI: Hint sızıntısı tespit edildi: {fc['id']} -> {fc['hint']}")
    assert leak_count == 0, f"HATA: Toplam {leak_count} akıl kartında ipucu sızıntısı var!"
    print("   Akıl kartı ipucu sızıntı kontrolü: 0 SIZINTI (KUSURSUZ).")

    # 5. MASTER DECK OBJESİNİ OLUŞTUR
    deck_data = {
        "id": "k1p-k1-19-dogumsal-kadin-erkek-genital-gelisim-anomalileri",
        "title": "Doğumsal Kadın/Erkek Genital Gelişim Anomalileri",
        "subtitle": "SRY ve SOX9 Testis Kaskadı, WNT4 ve FOXL2 Over Genetiği, DAX1 Dozaj Tersinmesi, Wolff ve Müller Kanal Farklılaşması, AMH ve DHT Biyokimyası, Chicago CGB Sınıflaması, Klinefelter, Turner ve Miks Gonadal Disgenezi, 5α-Redüktaz 2 Eksikliği, Androjen Duyarsızlık Sendromu (CAIS/PAIS), Konjenital Adrenal Hiperplazi (CYP21A2) ve Prenatal Deksametazon Yönetimi",
        "category": "Tıbbi Genetik",
        "department": "Tıbbi Genetik",
        "lecturer": "Dr. Öğr. Üyesi Serap Arslan (Tıbbi Genetik ABD)",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "slides": slides,
        "questions": questions,
        "flashcards": all_flashcards
    }

    # 6. RUNTIME ITEM OLUŞTUR
    os.makedirs(DECKS_ITEMS_DIR, exist_ok=True)
    item_path = os.path.join(DECKS_ITEMS_DIR, f"{deck_data['id']}.json")
    with open(item_path, "w", encoding="utf-8") as f:
        json.dump(deck_data, f, ensure_ascii=False, indent=2)
    print(f"5. Runtime Item yazıldı: {item_path}")

    # 7. MULTI-FORMAT PAKETLEME (packages/k1p-k1-19-dogumsal-kadin-erkek-genital-gelisim-anomalileri/)
    os.makedirs(PACKAGE_DIR, exist_ok=True)

    # 7a. manifest.json
    manifest = {
        "id": deck_data["id"],
        "title": deck_data["title"],
        "subtitle": deck_data["subtitle"],
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
            "blocks": "blocks.html",
            "content": "content.md"
        }
    }
    with open(os.path.join(PACKAGE_DIR, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    # 7b. content.md
    md_lines = [
        f"# {deck_data['title']}",
        f"**{deck_data['subtitle']}**\n",
        f"- **Ders / Departman:** {deck_data['department']}",
        f"- **Öğretim Üyesi:** {deck_data['lecturer']}",
        f"- **Kaynak:** {deck_data['sourcePdf']}",
        f"- **Slayt Sayısı:** {len(slides)} | **Soru Sayısı:** {len(questions)} | **Akıl Kartı:** {len(all_flashcards)}\n",
        "---"
    ]
    for idx, s in enumerate(slides):
        md_lines.append(f"\n## Slayt {idx+1}: {s['title']}\n")
        md_lines.append(s["content"])
        if s.get("elements"):
            md_lines.append("\n### İnteraktif Ögeler:")
            for el in s["elements"]:
                md_lines.append(f"- **Tip:** `{el['type']}`")
        if s.get("flashcards"):
            md_lines.append("\n### Checkpoint Akıl Kartları:")
            for fc in s["flashcards"]:
                md_lines.append(f"- **S:** {fc['front']}\n  - **C:** {fc['back']}\n  - *İpucu:* {fc['hint']}")
        md_lines.append("\n---")

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
        "    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; padding: 2rem; max-width: 900px; margin: 0 auto; color: #1e293b; background: #f8fafc; }",
        "    .slide-card { background: white; border-radius: 12px; padding: 1.5rem 2rem; margin-bottom: 2rem; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1); border: 1px solid #e2e8f0; }",
        "    .slide-header { display: flex; justify-content: space-between; align-items: baseline; border-bottom: 2px solid #e2e8f0; padding-bottom: 0.75rem; margin-bottom: 1rem; }",
        "    .slide-num { font-size: 0.875rem; font-weight: 700; color: #2563eb; text-transform: uppercase; }",
        "    .slide-title { font-size: 1.25rem; font-weight: 700; color: #0f172a; margin: 0; }",
        "    .content-body { white-space: pre-wrap; font-size: 0.95rem; color: #334155; }",
        "    .checkpoint { border-left: 5px solid #2563eb; background: #eff6ff; }",
        "    .badge { display: inline-block; padding: 0.25rem 0.5rem; background: #e0e7ff; color: #3730a3; border-radius: 6px; font-size: 0.75rem; font-weight: 600; margin-right: 0.5rem; }",
        "  </style>",
        "</head>",
        "<body>",
        f"  <h1>{deck_data['title']}</h1>",
        f"  <p><strong>{deck_data['subtitle']}</strong></p>",
        f"  <p><em>{deck_data['lecturer']}</em></p>"
    ]

    for idx, s in enumerate(slides):
        is_cp = "[TEKRAR SAYFASI" in s["title"]
        cp_class = " checkpoint" if is_cp else ""
        html_lines.append(f"  <article class=\"slide-card{cp_class}\">")
        html_lines.append("    <div class=\"slide-header\">")
        html_lines.append(f"      <span class=\"slide-num\">Slayt {idx+1}</span>")
        html_lines.append(f"      <h2 class=\"slide-title\">{s['title']}</h2>")
        html_lines.append("    </div>")
        clean_content = s["content"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        html_lines.append(f"    <div class=\"content-body\">{clean_content}</div>")
        if s.get("elements"):
            html_lines.append("    <div style=\"margin-top: 1rem;\">")
            for el in s["elements"]:
                html_lines.append(f"      <span class=\"badge\">{el['type']}</span>")
            html_lines.append("    </div>")
        html_lines.append("  </article>")

    html_lines.append("</body>")
    html_lines.append("</html>")

    with open(os.path.join(PACKAGE_DIR, "blocks.html"), "w", encoding="utf-8") as f:
        f.write("\n".join(html_lines))

    # 7d. structure.xml
    root = ET.Element("learningDeck", {
        "id": deck_data["id"],
        "title": deck_data["title"],
        "department": deck_data["department"],
        "slideCount": str(len(slides)),
        "questionCount": str(len(questions)),
        "flashcardCount": str(len(all_flashcards))
    })

    slides_node = ET.SubElement(root, "slides")
    for idx, s in enumerate(slides):
        s_node = ET.SubElement(slides_node, "slide", {
            "index": str(idx + 1),
            "id": s["id"],
            "title": s["title"],
            "isCheckpoint": "true" if "[TEKRAR SAYFASI" in s["title"] else "false"
        })
        content_node = ET.SubElement(s_node, "content")
        content_node.text = s["content"]

        if s.get("elements"):
            els_node = ET.SubElement(s_node, "interactiveElements")
            for el in s["elements"]:
                ET.SubElement(els_node, "element", {"type": el["type"]})

        if s.get("flashcards"):
            fcs_node = ET.SubElement(s_node, "flashcards")
            for fc in s["flashcards"]:
                fc_node = ET.SubElement(fcs_node, "flashcard", {"id": fc["id"], "category": fc.get("category", "")})
                ET.SubElement(fc_node, "front").text = fc["front"]
                ET.SubElement(fc_node, "back").text = fc["back"]
                ET.SubElement(fc_node, "hint").text = fc.get("hint", "")

    xml_str = ET.tostring(root, encoding="utf-8")
    parsed_xml = minidom.parseString(xml_str)
    pretty_xml = parsed_xml.toprettyxml(indent="  ", encoding="utf-8").decode("utf-8")

    with open(os.path.join(PACKAGE_DIR, "structure.xml"), "w", encoding="utf-8") as f:
        f.write(pretty_xml)

    print(f"6. Multi-format paket dosyaları oluşturuldu: {PACKAGE_DIR}")

    # 8. INTERACTIVE_LEARNING_DECKS.JSON DOSYASINI YERİNDE GÜNCELLE (INDEX 66)
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
    print("DERS 19 DECK BUILD VE PAKETLEME BAŞARIYLA TAMAMLANDI!")
    print("=" * 60)

if __name__ == "__main__":
    build_lesson_19_deck()
