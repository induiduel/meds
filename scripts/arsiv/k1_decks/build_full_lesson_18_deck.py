# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)
Master Deck Oluşturucu ve Çoklu Format Paketleyici.
100 Slayt, 10 Checkpoint (30 Akıl Kartı), 7 İnteraktif Eleman (%8+ Çeşitlilik),
168 Örnek Soru, Runtime Item ve Multi-format Paketleme (manifest, structure, blocks, content).
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

from scripts.k1_18_deck_data.helpers import make_flashcard
from scripts.k1_18_deck_data.section_1 import get_section_1_slides
from scripts.k1_18_deck_data.section_2 import get_section_2_slides
from scripts.k1_18_deck_data.section_3 import get_section_3_slides
from scripts.k1_18_deck_data.section_4 import get_section_4_slides
from scripts.k1_18_deck_data.section_5 import get_section_5_slides
from scripts.k1_18_deck_data.section_6 import get_section_6_slides
from scripts.k1_18_deck_data.section_7 import get_section_7_slides
from scripts.k1_18_deck_data.section_8 import get_section_8_slides
from scripts.k1_18_deck_data.section_9 import get_section_9_slides
from scripts.k1_18_deck_data.section_10 import get_section_10_slides

from scripts.enrich_k1_18_elements import apply_enrichment

# Dosya yolları
QUESTIONS_FILE = os.path.join(BASE_DIR, "meds/src/data/ornek_sorular/k1/k1-18-halk-sagligi-tarihcesi.json")
PACKAGE_DIR = os.path.join(BASE_DIR, "meds/src/data/decks/packages/k1p-k1-18-halk-sagligi-tarihcesi")
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
        "İlgili tarihsel halk sağlığı prensibini anımsayınız",
        "Ders notundaki kurucu kuralı düşününüz",
        "Kritik tıp tarihi bilgisini hatırlayınız",
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
                "k1-18-fc-01",
                "Winslow'un 1920 tanımında halk sağlığı hangi iki temel nitelikle tanımlanmıştır?",
                "Bilim ve sanattır.",
                "Halk sağlığının akademik ve sanatsal nitelemesi", "Halk Sağlığı Tanımı"
            ),
            make_flashcard(
                "k1-18-fc-02",
                "Hipokrat'ın humoral patoloji kuramında melankolik (hüzünlü) mizaçla ilişkilendirilen vücut sıvısı hangisidir?",
                "Kara safradır (Melanchole).",
                "Soğuk ve kuru nitelikteki dördüncü vücut sıvısı", "Antik Çağ Tıbbı"
            ),
            make_flashcard(
                "k1-18-fc-03",
                "Antik çağda bitkisel ve hayvansal karışımlarla galenik preparatlar hazırlayarak eczacılığın babası kabul edilen Bergamalı hekim kimdir?",
                "Galenos'tur (Bergamalı Galen).",
                "Roma imparatorlarının Bergama doğumlu hekimi", "Antik Çağ Tıbbı"
            )
        ],
        19: [
            make_flashcard(
                "k1-18-fc-04",
                "Bağdat'ta et astırarak en geç bozulan yere hastane inşa ettiren ve çiçek ile kızamığı ilk ayıran İslam hekimi kimdir?",
                "Ebubekir Razi'dir (er-Razi).",
                "Kokuşma kuramının öncüsü İslam hekimi", "İslam Tıbbı"
            ),
            make_flashcard(
                "k1-18-fc-05",
                "500 yıl boyunca Avrupa ve Doğu üniversitelerinde tıp eğitiminin vazgeçilmez temel ders kitabı olan El-Kanun fi't-Tıbb eserinin yazarı kimdir?",
                "İbn-i Sina'dır (Avicenna).",
                "Hekimlerin hükümdarı olarak anılan büyük bilgin", "İslam Tıbbı"
            ),
            make_flashcard(
                "k1-18-fc-06",
                "Salgın bölgelerinden gelen gemilerin limana girmeden önce açıkta 40 gün tecrit edilmesini ifade eden karantina terimi hangi dilden türemiştir?",
                "İtalyanca quaranta giorni (kırk gün) sözcüğünden türemiştir.",
                "Venedik liman tecrit süresi sözcük kökeni", "Salgınlar ve Karantina"
            )
        ],
        29: [
            make_flashcard(
                "k1-18-fc-07",
                "Kendi ürettiği yüksek çözünürlüklü el yapımı mikroskopla 1675 yılında hareket eden mikroorganizmaları ('animalcules') ilk kez gözlemleyen doğa bilimci kimdir?",
                "Antonie van Leeuwenhoek'tur.",
                "Delftli kumaş tüccarı ve mercek ustası", "Mikrobiyolojik Devrim"
            ),
            make_flashcard(
                "k1-18-fc-08",
                "Louis Pasteur'ün canlıların kendiliğinden oluşamayacağını (abiyogenezin imkansızlığını) kanıtlamak için tasarladığı ünlü deney düzeneği hangisidir?",
                "Kuğu boyunlu balon (Swan-neck flask) deneyidir.",
                "Tozu süzen kıvrık cam düzenek", "Mikrobiyolojik Devrim"
            ),
            make_flashcard(
                "k1-18-fc-09",
                "Robert Koch'un 1882 yılında keşfettiği ve dönemin Avrupa'sında her 7 ölümden birine yol açan bakteriyel enfeksiyon etkeni nedir?",
                "Tüberküloz basili (Mycobacterium tuberculosis / Koch basili).",
                "24 Mart günü anılan büyük akciğer hastalığı", "Bakteriyoloji"
            )
        ],
        39: [
            make_flashcard(
                "k1-18-fc-10",
                "Osmanlı'da hafif çiçek geçirenlerin püstül cerahatinin çizik atılarak sağlıklı çocuklara verilmesi yöntemine ne ad verilir?",
                "Variolasyondur (çiçekleme).",
                "İnsan çiçeği virüsüyle yapılan geleneksel aşılama", "Bağışıklama Tarihi"
            ),
            make_flashcard(
                "k1-18-fc-11",
                "1796 yılında sığır çiçeği (cowpox) kabarcığından aldığı sıvıyla James Phipps'i aşılayarak güvenli aşılamayı (vaccination) başlatan hekim kimdir?",
                "Edward Jenner'dır.",
                "Sığır çiçeği koruyuculuğunu keşfeden İngiliz kır hekimi", "Bağışıklama Tarihi"
            ),
            make_flashcard(
                "k1-18-fc-12",
                "1890 yılında difteri toksinine karşı bağışık atların serumunu kullanarak pasif bağışıklamayı başlatan ve ilk Nobel Tıp Ödülü'nü alan bilim insanı kimdir?",
                "Emil von Behring'dir.",
                "Difteri antitoksini serum terapisinin mimarı", "Bağışıklama Tarihi"
            )
        ],
        49: [
            make_flashcard(
                "k1-18-fc-13",
                "1854 Londra Broad Street kolera salgınında su tulumbasının kolunu söktürerek salgını durduran ve modern epidemiyolojinin babası sayılan hekim kimdir?",
                "John Snow'dur.",
                "Soho mahallesindeki ölümleri haritalayan hekim", "Çevre Sağlığı ve Epidemiyoloji"
            ),
            make_flashcard(
                "k1-18-fc-14",
                "1842 yılında hazırladığı sanitasyon raporuyla İngiltere'de 1848'de ilk Halk Sağlığı Yasası'nın çıkarılmasını sağlayan reformcu kimdir?",
                "Edwin Chadwick'tir.",
                "Kentsel altyapı ve kanalizasyon reformcusu", "Çevre Sağlığı ve Epidemiyoloji"
            ),
            make_flashcard(
                "k1-18-fc-15",
                "Etkeni ve sivrisinek vektörü henüz bilinmezken kına-kına ağacı kabuğuyla (kinin) tedavi edilen ilk bulaşıcı enfeksiyon hastalığı hangisidir?",
                "Sıtmadır (Malaria).",
                "Bataklık kaynaklı sanılan paraziter enfeksiyon", "Çevre Sağlığı ve Epidemiyoloji"
            )
        ],
        59: [
            make_flashcard(
                "k1-18-fc-16",
                "1747 yılında gemide skorbüt hastalarına limon ve portakal vererek ilk kontrollü klinik beslenme deneyini gerçekleştiren İskoç cerrah kimdir?",
                "James Lind'dir.",
                "Skorbütün narenciyeyle tedavisini kanıtlayan cerrah", "Beslenme ve Skorbüt"
            ),
            make_flashcard(
                "k1-18-fc-17",
                "1795 yılında İngiliz Kraliyet Donanması'nda tüm denizcilere günlük limon suyu verilmesini zorunlu kılarak skorbütü sıfırlayan hekim kimdir?",
                "Gilbert Blane'dir.",
                "Donanma Sağlık Heyeti Başkanı hekim", "Beslenme ve Skorbüt"
            ),
            make_flashcard(
                "k1-18-fc-18",
                "1700 yılında yazdığı De Morbis Artificum Diatriba eseriyle iş sağlığının babası kabul edilen ve hekimlere 'Ne iş yaparsınız?' sorusunu öğütleyen hekim kimdir?",
                "Bernardino Ramazzini'dir.",
                "İtalyan iş hekimliği öncüsü", "İş Sağlığı"
            )
        ],
        69: [
            make_flashcard(
                "k1-18-fc-19",
                "Sosyal patolojinin kurucusu Alfred Grotjahn'a göre bir hastalığın en önemli hastalık sayılmasının üç temel ölçütü nedir?",
                "En çok öldüren, en sık görülen ve en çok sakat bırakan hastalık olmasıdır.",
                "Grotjahn'ın üçlü önemli hastalık formülü", "Sosyal Hekimlik"
            ),
            make_flashcard(
                "k1-18-fc-20",
                "Yukarı Silezya tifüs salgınından sonra 'Tıp bir sosyal bilimdir ve politika geniş kapsamlı tıptan başka bir şey değildir' diyen ünlü patolog kimdir?",
                "Rudolf Virchow'dur.",
                "Hücresel patolojinin ve sosyal tıbbın Alman kurucusu", "Sosyal Hekimlik"
            ),
            make_flashcard(
                "k1-18-fc-21",
                "Dünya Sağlık Örgütü'nün (DSÖ) 1948 Anayasası'nda yer alan evrensel tanımına göre sağlık ne demektir?",
                "Yalnızca hastalık veya sakatlığın olmayışı değil; bedenen, ruhen ve sosyal yönden tam bir iyilik halidir.",
                "DSÖ'nün üç boyutlu tam iyilik tanımı", "Sosyal Hekimlik"
            )
        ],
        79: [
            make_flashcard(
                "k1-18-fc-22",
                "1930 yılında çıkarılan ve Türkiye'de bulaşıcı hastalıklarla mücadele ve koruyucu hekimliğin anayasası sayılan kanun hangisidir?",
                "1593 Sayılı Umumi Hıfzıssıhha Kanunu'dur.",
                "Dr. Refik Saydam'ın çıkardığı tarihi sağlık kanunu", "Türkiye'de Halk Sağlığı"
            ),
            make_flashcard(
                "k1-18-fc-23",
                "1961 yılında çıkarılan ve Türkiye'de sağlık ocakları sistemini, entegre koruyucu hekimliği ve kademeli sevk zincirini kuran kanunun numarası nedir?",
                "224 sayılı kanundur (Sağlık Hizmetlerinin Sosyalleştirilmesi Hakkında Kanun).",
                "Prof. Dr. Nusret Fişek'in mimarı olduğu tarihi yasa", "Türkiye'de Halk Sağlığı"
            ),
            make_flashcard(
                "k1-18-fc-24",
                "224 Sayılı Sosyalleştirme Kanunu kapsamında sağlık ocakları modeli ilk kez 1963 yılında pilot il olarak nerede uygulanmıştır?",
                "Muş ilidir.",
                "Doğu Anadolu'daki ilk pilot uygulama ili", "Türkiye'de Halk Sağlığı"
            )
        ],
        89: [
            make_flashcard(
                "k1-18-fc-25",
                "1978 yılında Kazakistan'da toplanan Alma-Ata Konferansı'nın ilan ettiği tarihi küresel hedef sloganı nedir?",
                "2000 Yılında Herkese Sağlık (Health for All by the Year 2000).",
                "Alma-Ata'nın evrensel hedef sloganı", "Alma-Ata Bildirgesi"
            ),
            make_flashcard(
                "k1-18-fc-26",
                "Alma-Ata Bildirgesi'nde toplumun tümüne ulaştırılması zorunlu kılınan Temel Sağlık Hizmetleri kaç ana bileşenden oluşur?",
                "8 ana bileşenden oluşur.",
                "Aşı, su, gıda, eğitim dahil asgari bileşen sayısı", "Alma-Ata Bildirgesi"
            ),
            make_flashcard(
                "k1-18-fc-27",
                "Halk sağlığı planlamasında sağlık kaynaklarının dağıtımında öncelik tanınması gereken en temel biyolojik ve sosyal risk grupları hangileridir?",
                "Gebe-emziren anneler, 0-5 yaş bebekler, yaşlılar ve ağır sanayi işçileridir.",
                "Biyolojik ve çevresel açıdan en hassas nüfus grupları", "Halk Sağlığı İlkeleri"
            )
        ],
        100: [
            make_flashcard(
                "k1-18-fc-28",
                "Hastalık riskini artıran sosyal, ekonomik ve kültürel yaşam tarzı özelliklerinin toplumda ve çocuklarda hiç oluşmamasını sağlamayı amaçlayan en erken korunma düzeyi hangisidir?",
                "Primordial korunmadır.",
                "Risk faktörünün oluşmasını baştan önleyen düzey", "Korunma Düzeyleri"
            ),
            make_flashcard(
                "k1-18-fc-29",
                "Asemptomatik bir kadında serviks kanserini henüz belirti vermeden yakalamak amacıyla yapılan rutin Pap-smear veya HPV-DNA taraması hangi korunma düzeyindedir?",
                "İkincil (sekonder) korunmadır.",
                "Pre-semptomatik erken tanı ve tarama düzeyi", "Korunma Düzeyleri"
            ),
            make_flashcard(
                "k1-18-fc-30",
                "Klinik diyabet tanısı almış bir hastada kangren ve bacak amputasyonunu önlemek amacıyla yapılan ayak bakımı eğitimi ve rehabilitasyon hangi korunma basamağına girer?",
                "Üçüncül (tersiyer) korunmadır.",
                "Sakatlığı sınırlandırma ve rehabilitasyon basamağı", "Korunma Düzeyleri"
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

def build_lesson_18_deck():
    print("=" * 60)
    print("KURUL 1 - DERS 18: HALK SAĞLIĞI TARİHÇESİ")
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
            q_id = q.get("id") or f"k1-18-q{len(questions)+1:02d}"
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
        "id": "k1p-k1-18-halk-sagligi-tarihcesi",
        "title": "Halk Sağlığı Tarihçesi",
        "subtitle": "Winslow ve Nusret Fişek Tanımları, Antik Çağ ve İslam Tıbbı, Mikrobiyolojik Devrim, Jenner ve Aşı Zaferleri, John Snow ve Çevre Sağlığı, Skorbüt ve İş Sağlığı, Sosyal Hekimlik, 224 Sayılı Sosyalleştirme Kanunu, Alma-Ata ve Korunma Düzeyleri",
        "category": "Halk Sağlığı",
        "department": "Halk Sağlığı",
        "lecturer": "Doç. Dr. Nergiz Sevinç (Halk Sağlığı ABD)",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
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

    # 7. MULTI-FORMAT PAKETLEME (packages/k1p-k1-18-halk-sagligi-tarihcesi/)
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

    # 8. INTERACTIVE_LEARNING_DECKS.JSON DOSYASINI YERİNDE GÜNCELLE (INDEX 65)
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
    print("DERS 18 DECK BUILD VE PAKETLEME BAŞARIYLA TAMAMLANDI!")
    print("=" * 60)

if __name__ == "__main__":
    build_lesson_18_deck()
