# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)
Master Deck Oluşturucu ve Multi-Format Paketleyici.
- 10 Bölüm, 100 Slayt, 10 Checkpoint (her birinde 3 akıl kartı -> toplam 30 akıl kartı).
- 7 İnteraktif Eleman Tipi (her biri en az %8.0 çeşitlilikte).
- Multi-format paketleme: manifest.json, structure.xml, blocks.html, content.md.
- Runtime item: meds/src/data/decks/items/k1p-k1-20-tromboz-patofizyolojisi.json
- Yerinde güncelleme: meds/src/data/interactive_learning_decks.json (İndeks 67) ve catalog.json.
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

from scripts.k1_20_deck_data.helpers import make_flashcard
from scripts.k1_20_deck_data.section_1 import get_section_1_slides
from scripts.k1_20_deck_data.section_2 import get_section_2_slides
from scripts.k1_20_deck_data.section_3 import get_section_3_slides
from scripts.k1_20_deck_data.section_4 import get_section_4_slides
from scripts.k1_20_deck_data.section_5 import get_section_5_slides
from scripts.k1_20_deck_data.section_6 import get_section_6_slides
from scripts.k1_20_deck_data.section_7 import get_section_7_slides
from scripts.k1_20_deck_data.section_8 import get_section_8_slides
from scripts.k1_20_deck_data.section_9 import get_section_9_slides
from scripts.k1_20_deck_data.section_10 import get_section_10_slides
from scripts.enrich_k1_20_elements import apply_enrichment

QUESTIONS_FILE = os.path.join(PROJECT_ROOT, "meds/src/data/ornek_sorular/k1/k1-20-tromboz-patofizyolojisi.json")
PACKAGE_DIR = os.path.join(PROJECT_ROOT, "meds/src/data/decks/packages/k1p-k1-20-tromboz-patofizyolojisi")
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
                "k1-20-fc-01",
                "Damar yaralanması sonrasında dakikalar içinde kanamayı geçici olarak durduran primer hemostaz tıkacının ana bileşeni nedir?",
                "Trombosit agregatları ve von Willebrand faktörüdür.",
                "Hücresel elemanlar ve subendotelyal yapıştırıcı glikoprotein", "Primer Hemostaz"
            ),
            make_flashcard(
                "k1-20-fc-02",
                "Sekonder hemostaz kaskadında polimerize fibrini çapraz bağlarla sağlamlaştıran nihai enzim hangisidir?",
                "Aktif Faktör XIII (Faktör XIIIa transglutaminaz).",
                "Son basamak polimerizasyon enzimi", "Sekonder Hemostaz"
            ),
            make_flashcard(
                "k1-20-fc-03",
                "Pıhtılaşmayı yaralanma bölgesiyle sınırlı tutan ve sağlam endotel yüzeyinde çalışan doğal antikoagülan mekanizmalar nelerdir?",
                "Prostasiklin/NO salınımı, Trombomodulin-Protein C yolağı ve Antitrombin III sistemidir.",
                "Sağlıklı damar iç yüzeyinin pıhtı önleyici savunma kalkanları", "Fizyolojik Antikoagülasyon"
            )
        ],
        19: [
            make_flashcard(
                "k1-20-fc-04",
                "Endotel yüzeyinde trombine bağlanarak onu prokoagülan bir enzimden antikoagülan bir aktivatöre dönüştüren transmembran reseptör hangisidir?",
                "Trombomodulindir.",
                "Vasküler iç yüzey frenleyici reseptörü", "Endotel Biyolojisi"
            ),
            make_flashcard(
                "k1-20-fc-05",
                "Sağlıklı endotelin trombosit agregasyonunu güçlü şekilde baskılayan ve vazodilatasyon yapan iki temel gaz ve prostaglandin medyatörü nedir?",
                "Nitrik Oksit (NO) ve Prostasiklindir (PGI2).",
                "Damar lümenini genişleten ve hücre kümelenmesini durduran çift salgı", "Endotel Medyatörleri"
            ),
            make_flashcard(
                "k1-20-fc-06",
                "Endotel hasarı veya denudasyonu sonrasında hemostazı başlatan ve trombosit GpIb reseptörüne bağlanan adeziv molekül nedir?",
                "Von Willebrand Faktördür (vWF).",
                "Weibel-Palade organelinden salınan subendotelyal köprü proteini", "Trombosit Adezyonu"
            )
        ],
        29: [
            make_flashcard(
                "k1-20-fc-07",
                "Virchow triyadında tanımlanan 'anormal kan akımı' hangi iki zıt hemodinamik paterni kapsar?",
                "Türbülans (girdaplı akım) ve Stazdır (kan durgunluğu/yavaşlaması).",
                "Dallanmalardaki kaotik burgu ile duraklama hali", "Hemodinamik Bozukluklar"
            ),
            make_flashcard(
                "k1-20-fc-08",
                "Venöz kapak ceplerinde kan akımının duraksaması ve lokal oksijenasyonun düşmesi endotelde hangi değişime yol açar?",
                "Endotelde adezyon molekülü ekspresyonuna ve prokoagülan fenotip gelişimine neden olur.",
                "Durgun vasküler yatakta hücresel yapışma eğilimi", "Venöz Staz"
            ),
            make_flashcard(
                "k1-20-fc-09",
                "Atriyal fibrilasyon ve ventrikül apeks anevrizmasında tromboz oluşumunu kolaylaştıran temel hemodinamik anormallik nedir?",
                "Kardiyak odacıklarda kanın laminer akımını kaybederek girdap yapması ve staza uğramasıdır.",
                "Boşluklardaki çalkantı ve duraksama hali", "Kardiyak Tromboz"
            )
        ],
        39: [
            make_flashcard(
                "k1-20-fc-10",
                "Kafkas ırkında en sık görülen herediter trombofili nedeni olan Faktör V Leiden mutasyonunun biyokimyasal temeli nedir?",
                "Faktör V'in 506. pozisyonundaki arjininin glutamine dönüşmesiyle Aktif Protein C'ye (APC) direnç kazanmasıdır.",
                "Arg506Gln değişimi sonucu enzimatik yıkılamama hali", "Herediter Trombofili"
            ),
            make_flashcard(
                "k1-20-fc-11",
                "Protrombin G20210A gen varyasyonunun plazmada yarattığı temel patofizyolojik değişiklik nedir?",
                "Protrombin mRNA kararlılığının artması sonucu kanda aşırı Faktör II (protrombin) birikmesidir.",
                "Hücresel transkript stabilitesiyle kaskad öncülünün yükselmesi", "Protrombin Mutasyonu"
            ),
            make_flashcard(
                "k1-20-fc-12",
                "Antitrombin III eksikliği olan bir hastaya intravenöz standart heparin verildiğinde gözlenen karakteristik laboratuvar cevapsızlığı nedir?",
                "aPTT süresinin uzamaması (heparin direnci gelişmesi).",
                "Kofaktör yokluğunda ilacın pıhtılaşma testini etkileyememesi", "Antitrombin Patolojisi"
            )
        ],
        49: [
            make_flashcard(
                "k1-20-fc-13",
                "Antifosfolipid antikor sendromunda (APS) laboratuvar test tüpü ile canlı vücudu arasındaki paradoks nedir?",
                "İn vitro ortamda aPTT testini uzatırken, in vivo ortamda güçlü tromboza yol açmasıdır.",
                "Tüpte kanamayı taklit eden fakat damarda pıhtı oluşturan antikor etkisi", "APS Paradoksu"
            ),
            make_flashcard(
                "k1-20-fc-14",
                "Heparin Kaynaklı Trombositopeni Tip 2'de (HIT-2) antikorların bağlandığı antijenik kompleks hangisidir?",
                "Trombosit Faktör 4 ile heparinin oluşturduğu komplekstir (PF4-Heparin).",
                "Kemokin ile antikoagülan polisakkaritin immünojenik birleşimi", "HIT Patogenezi"
            ),
            make_flashcard(
                "k1-20-fc-15",
                "HIT-2 şüphesi doğan bir hastada uygulanması gereken ilk acil klinik yaklaşım nedir?",
                "Tüm heparin formları derhal kesilmeli ve direkt trombin inhibitörü (argatroban) başlanmalıdır.",
                "İmmünolojik reaksiyonda medikasyonun durdurulup yenisinin verilmesi", "HIT Yönetimi"
            )
        ],
        59: [
            make_flashcard(
                "k1-20-fc-16",
                "Pankreas veya mide adenokarsinomu seyrinde görülen gezici venöz tromboflebit tablosuna ne ad verilir?",
                "Trousseau Sendromu (Tromboflebitis Migrans) adı verilir.",
                "Müsinöz karsinomlarda ekstremitelerde yer değiştiren venöz sertlikler", "Malignite Trombozu"
            ),
            make_flashcard(
                "k1-20-fc-17",
                "Yaygın İntravasküler Koagülasyon (DIC) patogenezinde mikrotrombüsler ile kanamanın aynı anda görülmesinin nedeni nedir?",
                "Trombositlerin ve koagülasyon faktörlerinin mikrodolaşımda hızla tükenmesidir (tüketim koagülopatisi).",
                "Hemostaz elemanlarının aşırı kullanım sonucu kanda bitmesi", "DIC Mekanizması"
            ),
            make_flashcard(
                "k1-20-fc-18",
                "DIC seyrinde fibrin ağlarına çarparak mekanik parçalanmaya uğrayan eritrositlere periferik yaymada ne ad verilir?",
                "Şistozit (parçalanmış kask hücresi) adı verilir.",
                "Mikroanjiyopatik hemolizin mikroskobik morfolojik bulgusu", "Hematopatoloji"
            )
        ],
        69: [
            make_flashcard(
                "k1-20-fc-19",
                "Pıhtılaşma faktörlerinin aktif membran yüzeylerine kalsiyum köprüleriyle bağlanabilmesi için hangi enzimatik modifikasyon gereklidir?",
                "K vitaminine bağımlı gama-glutamil karboksilasyon reaksiyonudur.",
                "Karaciğerde moleküllere kalsiyum afinitesi kazandıran süreç", "Biyokimyasal Modifikasyon"
            ),
            make_flashcard(
                "k1-20-fc-20",
                "Çapraz bağlı polimerize fibrinin plazmin tarafından eritilmesiyle açığa çıkan ve yüksek negatif prediktif değeri olan belirteç nedir?",
                "D-Dimer molekülüdür.",
                "Faktör XIIIa ile bağlanmış ağların lizis fragmanı", "Tromboz Belirteçleri"
            ),
            make_flashcard(
                "k1-20-fc-21",
                "Protrombinaz kompleksinin (Faktör Xa ve Va) katalitik olarak dönüştürdüğü substrat nedir?",
                "Protrombini (Faktör II) aktif trombine (Faktör IIa) dönüştürür.",
                "Kaskadın ana enzimini oluşturan kritik reaksiyon", "Pıhtılaşma Kaskadı"
            )
        ],
        79: [
            make_flashcard(
                "k1-20-fc-22",
                "Zahn çizgileri histopatolojik olarak hangi iki tabakanın ardışık diziliminden oluşur ve klinik anlamı nedir?",
                "Açık renkli trombosit-fibrin katmanları ile koyu renkli eritrosit katmanlarının ardışık dizilimidir. Pıhtının akan kanda ve antemortem (canlıda) oluştuğunu kanıtlar.",
                "Laminasyonlu mikroskobik desenin adli tıp önemi", "Trombüs Morfolojisi"
            ),
            make_flashcard(
                "k1-20-fc-23",
                "Postmortem pıhtıyı gerçek antemortem trombüsten ayıran en belirgin makroskobik özellikler nelerdir?",
                "Postmortem pıhtı duvara yapışmaz, jelatinöz-nemlidir, Zahn çizgisi içermez; yerçekimiyle çöken alt kırmızı (frenk üzümü) ve üst sarı plazma (tavuk yağı) tabakası gösterir.",
                "Cansız bedende lümende serbest duran iki renkli kütle", "Otopsi ve Adli Patoloji"
            ),
            make_flashcard(
                "k1-20-fc-24",
                "SLE hastalarında görülen Libman-Sacks endokarditini marantik endokardit ve enfektif endokarditten ayıran temel morfolojik özellik nedir?",
                "Kapak yaprakçıklarının her iki yüzünde (hem üst hem alt yüzeyinde) yerleşen küçük, verrüköz ve steril vejetasyonlar olmasıdır.",
                "Otoimmün valvülit nodüllerinin anatomik dağılımı", "Kapak Patolojisi"
            )
        ],
        89: [
            make_flashcard(
                "k1-20-fc-25",
                "Robbins patolojisine göre bir trombüsün karşılaşabileceği dört olası akıbet (kader) nelerdir?",
                "Propagasyon (ilerleme), Embolizasyon (kopma), Dissolüsyon (eritilme) ve Organizasyon/Rekanalizasyondur.",
                "Damar içi pıhtının izleyebileceği dört patofizyolojik yol", "Trombüsün Akıbeti"
            ),
            make_flashcard(
                "k1-20-fc-26",
                "Eski bir trombüsün t-PA tedavisine direnç kazanmasının moleküler ve hücresel gerekçesi nedir?",
                "Faktör XIIIa kovalent çapraz bağları, trombosit retraksiyonu ve fibroblastik kollajen infiltrasyonudur.",
                "İleri aşamadaki kütlenin kimyasal köprülerle pekişmesi", "Fibrinolitik Direnç"
            ),
            make_flashcard(
                "k1-20-fc-27",
                "DVT sonrası kapak tahribatı ve kronik venöz hipertansiyon sonucu gelişen tablonun adı ve derideki pigmentasyonun nedeni nedir?",
                "Post-Trombotik Sendromdur; derideki kahverengi renk ekstravaze eritrositlerin yıkımıyla oluşan hemosiderinden kaynaklanır.",
                "Valvüler yetmezlik ve dokuda biriken demirli pigment", "Kronik Venöz Sekel"
            )
        ],
        100: [
            make_flashcard(
                "k1-20-fc-28",
                "Virchow triyadının üçayağı nelerdir ve arteriyel ile venöz trombozda hangileri ön plandadır?",
                "Endotel hasarı, Anormal kan akımı ve Hiperkoagülabilitedir. Arterde endotel hasarı ve türbülans, vende ise staz ve hiperkoagülabilite baskındır.",
                "Klasik patoloji kuralındaki sacayağı dengesi", "Tromboz Büyük Özeti"
            ),
            make_flashcard(
                "k1-20-fc-29",
                "Aspirin, Heparin ve t-PA ilaçlarının hemostaz/tromboz üzerindeki etki hedefleri arasındaki fark nedir?",
                "Aspirin trombosit COX-1'ini bloke eder (antiplatelet). Heparin ATIII ile pıhtılaşma faktörlerini baskılar (antikoagülan). t-PA ise oluşmuş fibrin pıhtısını plazminle eritir (trombolitik).",
                "Üç farklı medikasyon grubunun moleküler hedefi", "Farmakoterapi İlkeleri"
            ),
            make_flashcard(
                "k1-20-fc-30",
                "DVT ve Pulmoner Emboli tanısında altın standart non-invaziv görüntüleme yöntemleri nelerdir?",
                "DVT için Kompresyon Doppler Ultrasonografi (basılamayan ven), Pulmoner Emboli için ise BT Pulmoner Anjiyografidir (dolum defekti).",
                "Ses dalgaları ve radyolojik lümen incelemesi", "Tanı Altın Standartları"
            )
        ]
    }
    return raw_cards

def build_lesson_20_deck():
    print("=" * 60)
    print("KURUL 1 - DERS 20: TROMBOZ PATOFİZYOLOJİSİ")
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
            q_id = q.get("id") or f"k1-20-q{len(questions)+1:02d}"
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
    for idx, s in enumerate(raw_slides):
        slide_num = idx + 1
        title = s.get("title", f"Slayt {slide_num}")
        content = s.get("content") or s.get("narrative", "")
        # Temiz interaktif elemanları al (type alanı olanlar)
        raw_elements = s.get("elements") or s.get("interactiveElements") or []
        clean_elements = [el for el in raw_elements if isinstance(el, dict) and el.get("type")]
        
        standardized_slides.append({
            "id": f"k1-20-s{slide_num:02d}",
            "slideNumber": slide_num,
            "title": title,
            "content": content,
            "sourcePdf": s.get("sourcePdf", "Tıbbi Patoloji ABD - Tromboz Patofizyolojisi Ders Notları"),
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
        "id": "k1p-k1-20-tromboz-patofizyolojisi",
        "title": "Tromboz Patofizyolojisi",
        "subtitle": "Virchow Triyadı, Endotel Disfonksiyonu ve Denudasyonu, Türbülans ve Venöz Staz Hemodinamiği, Faktör V Leiden ve Protrombin G20210A Herediter Trombofilileri, Antifosfolipid Antikor Sendromu, Heparin Kaynaklı Trombositopeni (HIT), Trousseau Sendromu ve DIC, Zahn Çizgileri, Arteriyel vs Venöz Trombüs Morfolojisi, Mural Trombüsler ve Vejetasyonlar, Postmortem Pıhtı Ayrımı, Trombüsün 4 Akıbeti, DVT ve Pulmoner Semer Emboli, Antiplateletler, Heparin, Varfarin ve DOAC Farmakoterapisi",
        "category": "Tıbbi Patoloji",
        "department": "Tıbbi Patoloji",
        "lecturer": "Prof. Dr. Hikmet Keleş (Tıbbi Patoloji ABD)",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
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

    # 7. MULTI-FORMAT PAKETLEME (packages/k1p-k1-20-tromboz-patofizyolojisi/)
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
        cls = "slide-card checkpoint" if is_cp else "slide-card"
        html_lines.append(f"  <div class=\"{cls}\">")
        html_lines.append("    <div class=\"slide-header\">")
        html_lines.append(f"      <span class=\"slide-num\">Slayt {idx+1}</span>")
        html_lines.append(f"      <h2 class=\"slide-title\">{s['title']}</h2>")
        html_lines.append("    </div>")
        html_lines.append(f"    <div class=\"content-body\">{s['content']}</div>")
        if s.get("elements"):
            html_lines.append("    <div style=\"margin-top: 1rem;\">")
            for el in s["elements"]:
                html_lines.append(f"      <span class=\"badge\">{el['type']}</span>")
            html_lines.append("    </div>")
        if s.get("flashcards"):
            html_lines.append("    <div style=\"margin-top: 1rem; padding: 1rem; background: #dbeafe; border-radius: 8px;\">")
            html_lines.append("      <strong>Checkpoint Akıl Kartları (3 Adet):</strong><ul>")
            for fc in s["flashcards"]:
                html_lines.append(f"        <li><strong>{fc['front']}</strong><br/>{fc['back']}</li>")
            html_lines.append("      </ul></div>")
        html_lines.append("  </div>")

    html_lines.append("</body></html>")
    with open(os.path.join(PACKAGE_DIR, "blocks.html"), "w", encoding="utf-8") as f:
        f.write("\n".join(html_lines))

    # 7d. structure.xml
    root = ET.Element("learningDeck", {"id": deck_data["id"]})
    meta = ET.SubElement(root, "metadata")
    ET.SubElement(meta, "title").text = deck_data["title"]
    ET.SubElement(meta, "subtitle").text = deck_data["subtitle"]
    ET.SubElement(meta, "category").text = deck_data["category"]
    ET.SubElement(meta, "department").text = deck_data["department"]
    ET.SubElement(meta, "lecturer").text = deck_data["lecturer"]
    ET.SubElement(meta, "sourcePdf").text = deck_data["sourcePdf"]

    slides_node = ET.SubElement(root, "slides", {"count": str(len(slides))})
    for idx, s in enumerate(slides):
        s_node = ET.SubElement(slides_node, "slide", {"index": str(idx+1), "id": s["id"]})
        ET.SubElement(s_node, "title").text = s["title"]
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

    # 8. INTERACTIVE_LEARNING_DECKS.JSON DOSYASINI YERİNDE GÜNCELLE (INDEX 67)
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
    print("DERS 20 DECK BUILD VE PAKETLEME BAŞARIYLA TAMAMLANDI!")
    print("=" * 60)

if __name__ == "__main__":
    build_lesson_20_deck()
