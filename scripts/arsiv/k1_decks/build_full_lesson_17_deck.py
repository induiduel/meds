# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Enfeksiyonlarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)
Master Deck Oluşturucu ve Çoklu Format Paketleyici.
100 Slayt, 10 Checkpoint (30 Akıl Kartı), 7 İnteraktif Eleman (%8+ Çeşitlilik),
204 Örnek Soru, Runtime Item ve Multi-format Paketleme (manifest, structure, blocks, content).
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

from scripts.k1_17_deck_data.helpers import make_flashcard
from scripts.k1_17_deck_data.section_1 import get_section_1_slides
from scripts.k1_17_deck_data.section_2 import get_section_2_slides
from scripts.k1_17_deck_data.section_3 import get_section_3_slides
from scripts.k1_17_deck_data.section_4 import get_section_4_slides
from scripts.k1_17_deck_data.section_5 import get_section_5_slides
from scripts.k1_17_deck_data.section_6 import get_section_6_slides
from scripts.k1_17_deck_data.section_7 import get_section_7_slides
from scripts.k1_17_deck_data.section_8 import get_section_8_slides
from scripts.k1_17_deck_data.section_9 import get_section_9_slides
from scripts.k1_17_deck_data.section_10 import get_section_10_slides

from scripts.enrich_k1_17_elements import apply_enrichment

# Dosya yolları
QUESTIONS_FILE = os.path.join(BASE_DIR, "meds/src/data/ornek_sorular/k1/k1-17-cinsel-yolla-bulasan-enfeksiyonlarda-tedavi.json")
PACKAGE_DIR = os.path.join(BASE_DIR, "meds/src/data/decks/packages/k1p-k1-17-cinsel-yolla-bulasan-enfeksiyonlarda-tedavi")
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
        "İlgili enfeksiyon prensibini anımsayınız",
        "Ders notundaki farmakoterapötik kuralı düşününüz",
        "Kritik klinik bilgiyi hatırlayınız",
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
                "k1-17-fc-01",
                "Cinsel yolla bulaşan enfeksiyonlarda kadınlarda anatomik ve fizyolojik yatkınlığın temel nedenleri nelerdir?",
                "Geniş mukozal yüzey alanı, vajinal asidik dengenin bozulabilmesi ve servikal kolumnar epitelin ektropiyonudur.",
                "Kadın genital mukozal yapısı ve hormonal hassasiyet", "CYBE Epidemiyolojisi"
            ),
            make_flashcard(
                "k1-17-fc-02",
                "CYBE etkenlerinden hangileri zorunlu hücre içi mikroorganizmadır?",
                "Chlamydia trachomatis ve virüslerdir (HSV, HPV).",
                "Zorunlu intraselüler çoğalan patojenler", "CYBE Epidemiyolojisi"
            ),
            make_flashcard(
                "k1-17-fc-03",
                "DSÖ'nün CYBE yönetiminde laboratuvar beklenmeksizin klinik sendromlara göre ampirik tedavi verilmesi yaklaşımına ne ad verilir?",
                "Sendromik yönetim yaklaşımıdır.",
                "Semptom ve klinik bulgulara dayalı hızlı tedavi protokolü", "CYBE Epidemiyolojisi"
            )
        ],
        19: [
            make_flashcard(
                "k1-17-fc-04",
                "Bakteriyel vajinozis tanısında Amsel kriterlerinin 4 bileşeni nelerdir?",
                "Homojen gri-beyaz akıntı, vajinal pH > 4.5, pozitif Whiff amin testi ve mikroskopide clue cell (ipucu hücresi) varlığıdır.",
                "Dörtlü tanısal klinik ve mikroskopik ölçüt", "Vajinal ve Servikal Sendromlar"
            ),
            make_flashcard(
                "k1-17-fc-05",
                "Normal vajinada laktobasillerin glikojeni fermente ederek ürettiği ve asidik pH'yı (3.8-4.5) sağlayan temel asit nedir?",
                "Laktik asittir.",
                "Koruyucu vajinal asitliği sağlayan organik bileşik", "Vajinal ve Servikal Sendromlar"
            ),
            make_flashcard(
                "k1-17-fc-06",
                "Mukopürülan servisitin en sık iki bakteriyel etkeni hangileridir?",
                "Chlamydia trachomatis ve Neisseria gonorrhoeae'dir.",
                "Endoservikal kolumnar epiteli tutan iki klasik bakteri", "Vajinal ve Servikal Sendromlar"
            )
        ],
        29: [
            make_flashcard(
                "k1-17-fc-07",
                "Üretrit sendromunda gonokokal ve nongonokokal üretrit ayrımında üretral yaymanın Gram boyamasında ne aranır?",
                "Polimorfonükleer lökositler içinde Gram negatif fasulye tanesi şeklinde intraselüler diplokoklar gonore lehinedir.",
                "Lökosit içi çiftli boyanma morfolojisi", "Üretrit Sendromu"
            ),
            make_flashcard(
                "k1-17-fc-08",
                "Nongonokokal üretritin (NGU) en sık bakteriyel etkeni hangisidir?",
                "Chlamydia trachomatis (serovar D-K) bakterisidir.",
                "Mukoid akıntılı NGU'nun bir numaralı sebebi", "Üretrit Sendromu"
            ),
            make_flashcard(
                "k1-17-fc-09",
                "Doksisiklin ve azitromisine yanıtsız, makrolid direnci yüksek, hücre duvarsız atipik NGU etkeni hangisidir?",
                "Mycoplasma genitalium'dur (tedavide Moksifloksasin kullanılır).",
                "Dirençli mikoplazma türü", "Üretrit Sendromu"
            )
        ],
        39: [
            make_flashcard(
                "k1-17-fc-10",
                "Islak damla mikroskopisinde kırbaç benzeri aktif hareket eden kamçılı trofozoitlerin görüldüğü CYBE etkeni nedir?",
                "Trichomonas vaginalis parazitidir.",
                "Kamçılı tek hücreli paraziter etken", "Trikomoniyazis Tedavisi"
            ),
            make_flashcard(
                "k1-17-fc-11",
                "Trikomoniyazisin birinci tercih tedavisi nedir ve partner yaklaşımı nasıl olmalıdır?",
                "Metronidazol 2 g oral tek doz (veya 2x500 mg 7 gün); cinsel partner semptomsuz olsa bile mutlaka eşzamanlı tedavi edilmelidir.",
                "Tek doz nitroimidazol ve ping-pong önleme ilkesi", "Trikomoniyazis Tedavisi"
            ),
            make_flashcard(
                "k1-17-fc-12",
                "Metronidazol kullanımı sırasında alkol alındığında şiddetli taşikardi, bulantı ve hipotansiyonla seyreden reaksiyonun adı nedir?",
                "Disülfiram benzeri reaksiyondur (aldehit dehidrogenaz inhibisyonuna bağlıdır).",
                "Asetaldehit birikimi toksisitesi", "Trikomoniyazis Tedavisi"
            )
        ],
        49: [
            make_flashcard(
                "k1-17-fc-13",
                "Chlamydia trachomatis'in hücre dışı enfeksiyöz formu ile hücre içi replike olan metabolik aktif formu hangileridir?",
                "Hücre dışı enfeksiyöz form Elementer Cisimcik (EB); hücre içi replike olan form Retiküler Cisimciktir (RB).",
                "İki farklı biyolojik yaşam evresi", "Klamidya Tedavisi"
            ),
            make_flashcard(
                "k1-17-fc-14",
                "Gebe olmayan erişkinde komplike olmamış klamidya enfeksiyonunun standart tedavisi nedir?",
                "Doksisiklin 100 mg oral 2x1 (7 gün) VEYA Azitromisin 1 g oral tek dozdur.",
                "Yedi günlük tetrasiklin veya tek doz makrolid", "Klamidya Tedavisi"
            ),
            make_flashcard(
                "k1-17-fc-15",
                "Chlamydia trachomatis L1-L3 serovarlarına bağlı gelişen ve kasıkta oluk belirtisi (groove sign) yapan derin lenfatik enfeksiyon nedir?",
                "Lenfogranüloma Venereum'dur (LGV; tedavisi 21 gün Doksisiklindir).",
                "Oluk belirtili derin lenfadenopatik hastalık", "Klamidya Tedavisi"
            )
        ],
        59: [
            make_flashcard(
                "k1-17-fc-16",
                "Neisseria gonorrhoeae'nin kesin tanısında kullanılan zenginleştirilmiş seçici besiyerinin adı nedir?",
                "Thayer-Martin besiyeri veya çukulata agardır.",
                "Karbondioksitli ortamda üreyen seçici gonokok agarı", "Gonokok Tedavisi"
            ),
            make_flashcard(
                "k1-17-fc-17",
                "Gonore tedavisinde küresel direnç ve klamidya koinfeksiyonu nedeniyle güncel standart birinci tercih rejim nedir?",
                "Seftriakson 250 mg İM tek doz + Azitromisin 1 g oral tek dozdur.",
                "Üçüncü kuşak sefalosporin ve makrolid ikilisi", "Gonokok Tedavisi"
            ),
            make_flashcard(
                "k1-17-fc-18",
                "Dissemine gonokokal enfeksiyonun (DGE) klasik klinik triadı nedir?",
                "Poliartralji/gezici artrit, tenosinovit ve parmak/eklem üzerinde hemorajik-nekrotik püstüllerdir.",
                "Artrit, tenosinovit ve deri döküntüsü üçlüsü", "Gonokok Tedavisi"
            )
        ],
        69: [
            make_flashcard(
                "k1-17-fc-19",
                "Pelvik Enflamatuar Hastalıkta (PİH) bimanuel muayenede serviksin hareket ettirilmesiyle oluşan patognomonik ağrıya ne ad verilir?",
                "Servikal hareket hassasiyetidir (Frenk kelebeği / Chandelier bulgusu).",
                "Muayenede hastayı zıplatan servikal ağrı işareti", "PİH ve Epididimit"
            ),
            make_flashcard(
                "k1-17-fc-20",
                "PİH komplikasyonu olarak perihepatik adezyonlara bağlı laparoskopide görülen 'keman teli' manzarasına ne ad verilir?",
                "Fitz-Hugh-Curtis sendromudur.",
                "Glisson kapsülü ile periton arası fibröz bantlar", "PİH ve Epididimit"
            ),
            make_flashcard(
                "k1-17-fc-21",
                "35 yaş altı genç erkekte akut epididimitin en sık iki etkeni hangileridir?",
                "Chlamydia trachomatis ve Neisseria gonorrhoeae'dir.",
                "Genç erkekteki iki ana üretral bakteriyel patojen", "PİH ve Epididimit"
            )
        ],
        79: [
            make_flashcard(
                "k1-17-fc-22",
                "Haemophilus ducreyi'nin Gram boyamasında bakterilerin paralel dizilerek oluşturduğu karakteristik manzaraya ne ad verilir?",
                "Balık sürüsü (school of fish) veya tren yolu manzarasıdır.",
                "Mikroskopideki paralel kokobasil kümelenmesi", "Şankroid ve Sifilis"
            ),
            make_flashcard(
                "k1-17-fc-23",
                "Şankroid ülseri ile primer sifilis şankrı arasındaki ağrı ve taban kıvamı farkı nasıldır?",
                "Şankroid ülseri yumuşak tabanlı, sarı cerahatli ve aşırı ağrılıdır; sifilis şankrı sert endüre tabanlı, temiz yüzeyli ve tamamen ağrısızdır.",
                "Ağrılı yumuşak cerahat vs ağrısız sert kıkırdak zıtlığı", "Şankroid ve Sifilis"
            ),
            make_flashcard(
                "k1-17-fc-24",
                "Şankroid tedavisinde birinci tercih antibiyotikler nelerdir ve fluktuan bubonlara cerrahi yaklaşım nasıl olmalıdır?",
                "Azitromisin 1 g oral tek doz veya Seftriakson 250 mg İM tek dozdur; fluktuan bubonlar neşterle kesilmez, kalın iğneyle aspire edilir.",
                "Tek doz antibiyotik ve fistül önleyici iğne ponksiyonu", "Şankroid ve Sifilis"
            )
        ],
        89: [
            make_flashcard(
                "k1-17-fc-25",
                "Genital herpes virüsünün (HSV-2) sinir sisteminde ömür boyu latent kaldığı anatomik bölge neresidir?",
                "Sakral duyusal ganglionlardır (S2-S4).",
                "Genital dermatomları inerve eden duyu gangliyonu", "Viral CYBE"
            ),
            make_flashcard(
                "k1-17-fc-26",
                "Genital herpesin ilk atağında standart antiviral rejimler nelerdir?",
                "Valasiklovir 2x1000 mg (7-10 gün) VEYA Asiklovir 3x400 mg (7-10 gün); latent virüsü eradike edemez.",
                "Nükleozid analoğu antiviral tedavi süresi", "Viral CYBE"
            ),
            make_flashcard(
                "k1-17-fc-27",
                "Kondiloma akuminata tedavisinde kullanılan ancak antimitotik ve teratojenik olduğu için gebelikte kesinlikle kontrendike olan topikal ajan hangisidir?",
                "Podofilotoksindir (gebede Kriyoterapi ve TCA tercih edilir).",
                "Mikrotübül zehiri antimitotik solüsyon", "Viral CYBE"
            )
        ],
        100: [
            make_flashcard(
                "k1-17-fc-28",
                "Cinsel yolla bulaşan bir enfeksiyon saptandığında hastanın geriye dönük son kaç gündeki partnerleri taranmalı ve tedavi edilmelidir?",
                "Son 60 gün içindeki tüm cinsel partnerler ampirik tedaviye alınmalıdır.",
                "Geriye dönük temaslı taramasındaki iki aylık süre kuralı", "CYBE Klinik Yönetimi"
            ),
            make_flashcard(
                "k1-17-fc-29",
                "CYBE tedavisi alan hastalara tek doz dahi olsa reenfeksiyonu önlemek için kaç gün zorunlu cinsel perhiz verilir?",
                "7 gün boyunca tam cinsel perhiz uygulanmalıdır.",
                "Tedavi sonrası zorunlu bir haftalık temas yasağı", "CYBE Klinik Yönetimi"
            ),
            make_flashcard(
                "k1-17-fc-30",
                "Gebelikte kemik büyüme geriliği ve bebek dişlerinde kalıcı sarı-kahverengi lekelenme yaptığı için kesinlikle kontrendike olan antibiyotik grubu hangisidir?",
                "Tetrasiklinler ve doksisiklindir (gebede klamidya için tek doz Azitromisin verilir).",
                "Kalsiyum şelasyonu yapan teratojen antibiyotik sınıfı", "CYBE Klinik Yönetimi"
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

def build_lesson_17_deck():
    print("=" * 60)
    print("KURUL 1 - DERS 17: CİNSEL YOLLA BULAŞAN ENFEKSİYONLARDA TEDAVİ")
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
            q_id = q.get("id") or f"k1-17-q{len(questions)+1:02d}"
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
        "id": "k1p-k1-17-cinsel-yolla-bulasan-enfeksiyonlarda-tedavi",
        "title": "Cinsel Yolla Bulaşan Enfeksiyonlarda Tedavi",
        "subtitle": "CYBE Epidemiyolojisi, Vajinit/Servisit, Üretrit Sendromu, Trikomoniyazis, Klamidya, Gonore, PİH, Epididimit, Genital Ülserler, Şankroid, Sifilis, Genital Herpes (HSV), HPV, Partner Tedavisi ve Gebelikte Farmakoterapi",
        "category": "Enfeksiyon Hastalıkları",
        "department": "Enfeksiyon Hastalıkları",
        "lecturer": "Dr. Öğr. Üyesi Rüveyda Korkmazer (Enfeksiyon Hastalıkları ABD)",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
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

    # 7. MULTI-FORMAT PAKETLEME (packages/k1p-k1-17-cinsel-yolla-bulasan-enfeksiyonlarda-tedavi/)
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

    # 8. INTERACTIVE_LEARNING_DECKS.JSON DOSYASINI YERİNDE GÜNCELLE (INDEX 64)
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
            print(f"7. interactive_learning_decks.json sonuna yeni deste olarak eklendi.")

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
    print("DERS 17 DECK BUILD VE PAKETLEME BAŞARIYLA TAMAMLANDI!")
    print("=" * 60)

if __name__ == "__main__":
    build_lesson_17_deck()
