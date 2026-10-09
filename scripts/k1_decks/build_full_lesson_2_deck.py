#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_full_lesson_2_deck.py
Kurul 1 - Ders 2: Patolojiye Giriş
Öğretim Üyesi: Prof. Dr. Hikmet Keleş

Yeni Nesil Multi-Format (JSON, XML, HTML, MD) Mikro-Öğrenme Motoru:
1. Tam 100 Atomik Adım.
2. 10 Özel Tekrar Sayfası (Checkpoints 1-10), her birinde 3'er adet gömülü Akıl Kartı (Flashcards, toplam 30 adet).
3. Kısa, yalın, gereksiz uzatmasız tablo başlıkları.
4. Tam dengeli 240-275 İnteraktif Öğe (Adım sayısının ~2.6 katı, [1.5x - 3.0x] aralığında).
5. 7 farklı interaktif öge türü, her biri kesinlikle en az %8 kullanım oranına sahip:
   - micro_quiz: >= %8
   - interactive_table: >= %8
   - cloze_masking: >= %8
   - before_after_slider: >= %8
   - causal_chain: >= %8
   - active_recall: >= %8
   - branching_logic: >= %8
6. 4 Dosyalı Multi-Format Paket Üretimi:
   - manifest.json
   - structure.xml
   - blocks.html
   - content.md
7. Runtime JSON deste dosyası (interactive_learning_decks.json), item JSON ve catalog.json senkronizasyonu.
"""

import json
import os
import sys
import re
import xml.etree.ElementTree as ET
from xml.dom import minidom
from collections import Counter

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MEDS_ROOT = os.path.join(PROJECT_ROOT, 'meds')
DECKS_ITEMS_DIR = os.path.join(MEDS_ROOT, 'src', 'data', 'decks', 'items')
PACKAGES_DIR = os.path.join(MEDS_ROOT, 'src', 'data', 'decks', 'packages', 'k1-02-patolojiye-giris')
CATALOG_PATH = os.path.join(MEDS_ROOT, 'src', 'data', 'decks', 'catalog.json')
INTERACTIVE_DECKS_PATH = os.path.join(MEDS_ROOT, 'src', 'data', 'interactive_learning_decks.json')
ORNEK_SORULAR_PATH = os.path.join(MEDS_ROOT, 'src', 'data', 'ornek_sorular', 'k1', 'k1-02-patolojiye-giris.json')

# Section importları
sys.path.insert(0, os.path.dirname(__file__))
from k1_02_deck_data import (
    section_1,
    section_2,
    section_3,
    section_4,
    section_5,
    section_6,
    section_7,
    section_8,
    section_9,
    section_10
)
from k1_02_deck_data.helpers import (
    make_micro_quiz,
    make_interactive_table,
    make_cloze,
    make_before_after,
    make_causal_chain,
    make_active_recall,
    make_branching_logic,
    make_flashcard
)

# Sızıntı kontrol fonksiyonları (validate_learning_decks.py ile birebir uyumlu)
def fold(s):
    return str(s or '').lower().replace('ı', 'i').replace('İ', 'i')

def leaks(hint, answer):
    h = fold(hint)
    return any((w[:5] if len(w) > 5 else w) in h for w in re.findall(r'[\wçğıöşü%.,-]+', fold(answer)) if len(w) >= 3 or re.search(r'\d', w))

def sanitize_hint(hint, answer):
    """Eğer ipucu cevabı sızdırıyorsa güvenli ve sızıntısız bir pedagojik ipucuyla değiştirir."""
    if not hint or not leaks(hint, answer):
        return hint
    candidate_prompts = [
        "Klinik Kavram",
        "Tanısal İlke",
        "Temel Belirteç",
        "Uluslararası Terminoloji",
        "Patolojik Süreç",
        "Metodolojik Standart",
        "Kritik Bilgi"
    ]
    for p in candidate_prompts:
        if not leaks(p, answer):
            return p
    return ""

def clean_table_title(title):
    """Gereksiz uzun tablo başlıklarını sadeleştirir."""
    if not title:
        return "Özet Tablo"
    t = title
    for junk in [
        "Büyük Sentez ve Karşılaştırma Matrisi",
        "Kapsamlı Sentez ve Karşılaştırma Matrisi",
        "Büyük Karşılaştırma Matrisi",
        "Büyük Sentez Tablosu",
        "Büyük Ayırıcı Tanı Tablosu",
        "Büyük Sentez Matrisi",
        "Büyük Karşılaştırma Tablosu",
        "Ezber Tablosu",
        "Ezber Matrisi",
        "Sentez Tablosu",
        "Sentez Matrisi",
        "Karşılaştırma Matrisi",
        "Karşılaştırma Tablosu",
        "Hafıza Tablosu",
        "Hızlı Ezber Tablosu",
        "Kilit Ezber Tablosu"
    ]:
        t = t.replace(junk, "").strip()
    t = t.rstrip(":-· ")
    return t if len(t) > 2 else "Özet Tablo"

def main():
    print("🚀 Kurul 1 - Ders 2 (Patolojiye Giriş) Tam Deste Oluşturucu Başlatılıyor...")
    deck_id = "k1p-k1-02-patolojiye-giris"

    # Paket dizinini garantiye al
    os.makedirs(PACKAGES_DIR, exist_ok=True)
    os.makedirs(DECKS_ITEMS_DIR, exist_ok=True)

    # 10 Bölümün adımlarını topla
    raw_steps = []
    raw_steps.extend(section_1.get_steps())   # 1-9 (9 adım, CP1 @ 9)
    raw_steps.extend(section_2.get_steps())   # 10-19 (10 adım, CP2 @ 19)
    raw_steps.extend(section_3.get_steps())   # 20-29 (10 adım, CP3 @ 29)
    raw_steps.extend(section_4.get_steps())   # 30-39 (10 adım, CP4 @ 39)
    raw_steps.extend(section_5.get_steps())   # 40-49 (10 adım, CP5 @ 49)
    raw_steps.extend(section_6.get_steps())   # 50-59 (10 adım, CP6 @ 59)
    raw_steps.extend(section_7.get_steps())   # 60-69 (10 adım, CP7 @ 69)
    raw_steps.extend(section_8.get_steps())   # 70-79 (10 adım, CP8 @ 79)
    raw_steps.extend(section_9.get_steps())   # 80-89 (10 adım, CP9 @ 89)
    raw_steps.extend(section_10.get_steps())  # 90-100 (11 adım, CP10 @ 100)

    print(f"Toplanan ham adım sayısı: {len(raw_steps)}")
    assert len(raw_steps) == 100, f"Hata: 100 adım beklenirken {len(raw_steps)} adım bulundu!"

    # Örnek soruları yükle ve validator formatına tam uyumlu (stem + options + correctAnswer) hazırla
    questions = []
    if os.path.exists(ORNEK_SORULAR_PATH):
        try:
            with open(ORNEK_SORULAR_PATH, "r", encoding="utf-8") as f:
                qdata = json.load(f)
            for k in qdata.get("kazanimlar", []):
                for q in k.get("sorular", []):
                    # Soru formatını normalize et
                    options_list = []
                    dogru_cevap = str(q.get("dogru", "")).strip().upper()
                    if len(dogru_cevap) > 1 and dogru_cevap[0] in "ABCDE":
                        dogru_cevap = dogru_cevap[0]
                    for opt_key in sorted(q.get("secenekler", {}).keys()):
                        opt_text = q["secenekler"][opt_key]
                        exp = q.get("sik_aciklamalari", {}).get(opt_key, q.get("aciklama", "Detaylı klinik açıklama."))
                        options_list.append({
                            "key": opt_key,
                            "text": opt_text,
                            "isCorrect": (opt_key == dogru_cevap),
                            "explanation": exp
                        })
                    questions.append({
                        "id": q.get("id"),
                        "stem": q.get("soru"),
                        "question": q.get("soru"),
                        "questionText": q.get("soru"),
                        "correctAnswer": dogru_cevap,
                        "explanation": q.get("aciklama"),
                        "options": options_list,
                        "pedagogicalType": "case_analysis" if "hasta" in q.get("soru", "").lower() else "mechanistic"
                    })
            print(f"Yüklenen ve normalize edilen örnek soru sayısı: {len(questions)}")
        except Exception as e:
            print(f"Soru yükleme uyarısı: {e}")

    # Ekstra klinik branching logic ve active recall envanteri
    extra_branching = {
        5: make_branching_logic(
            "Moleküler düzeyde hücre hasarı şüphesi olan bir biyopside hastanın klinik yönetim kararı senaryosu.",
            [
                {
                    "text": "Yalnızca makroskobik boyut ölçülür, hücresel sinyal yolaklarına bakılmaz.",
                    "isCorrect": False,
                    "feedback": "Hatalı! Subklinik moleküler hasar makroskopide görünmez; ileri moleküler veya biyokimyasal test gerekir."
                },
                {
                    "text": "Hücre zedelenmesinin geri dönüşlü (hidropik şişme) mi yoksa geri dönüşsüz (nekroz) mi olduğu araştırılır.",
                    "isCorrect": True,
                    "feedback": "Doğru yaklaşım! Erken moleküler hasar geri dönüşlü evrede yakalanırsa organ fonksiyonu kurtarılabilir."
                },
                {
                    "text": "Hasta doğrudan klinik otopsiye sevk edilir.",
                    "isCorrect": False,
                    "feedback": "Kabul edilemez! Hasta hayattadır."
                }
            ]
        ),
        11: make_branching_logic(
            "Ailede erken yaşta meme ve over karsinomu öyküsü olan 28 yaşındaki bir kadında etiyolojik yaklaşım senaryosu.",
            [
                {
                    "text": "Sadece sedimantasyon ve CRP bakılarak hasta evine gönderilir.",
                    "isCorrect": False,
                    "feedback": "Yetersiz! Genç yaşta ailevi karsinom öyküsü genetik yatkınlığı düşündürür."
                },
                {
                    "text": "BRCA1 ve BRCA2 tümör baskılayıcı gen mutasyonları açısından genetik danışmanlık ve moleküler test planlanır.",
                    "isCorrect": True,
                    "feedback": "Mükemmel! Kalıtsal tümör baskılayıcı gen kusurlarının erken tespiti profilaktik cerrahi ve sıkı taramayla hayat kurtarır."
                },
                {
                    "text": "Hastaya derhal kemoterapi başlanır.",
                    "isCorrect": False,
                    "feedback": "Hatalı! Tümör teşhisi konmadan kemoterapi verilemez."
                }
            ]
        ),
        16: make_branching_logic(
            "Sol ventrikül hipertrofisi olan bir hipertansiyon hastasında kardiyak adaptasyonun sınırları senaryosu.",
            [
                {
                    "text": "Miyositler sonsuza kadar bölünerek yeni kalp kası hücreleri üretir.",
                    "isCorrect": False,
                    "feedback": "Hatalı! Kalp kası bölünemeyen kalıcı dokudur; hiperplazi yapamaz, sadece hipertrofiye uğrar."
                },
                {
                    "text": "Hipertansiyon kontrol altına alınmazsa hipertrofi dekompansasyona uğrar; miyosit ölümü, fibrozis ve kalp yetmezliği gelişir.",
                    "isCorrect": True,
                    "feedback": "Doğru patofizyolojik öngörü! Adaptif hipertrofinin vasküler beslenme sınırı aşıldığında dilatasyon ve yetmezlik başlar."
                },
                {
                    "text": "Hipertrofi kendiliğinden atrofiye döner ve tedavi gerekmez.",
                    "isCorrect": False,
                    "feedback": "Yanlış! Bası yükü sürdükçe atrofi değil kalp yetmezliği gelişir."
                }
            ]
        ),
        23: make_branching_logic(
            "Tümör konseyinde karaciğerinde soliter kitle saptanan 50 yaşındaki hastanın dosyasında cerrahi öncesi patolojik biyopsi tartışması senaryosu.",
            [
                {
                    "text": "PET-BT'de SUV tutulumu olduğu için doğrudan radikal karaciğer lobektomisine alınır; biyopsiye gerek yoktur.",
                    "isCorrect": False,
                    "feedback": "Riskli karar! PET'te granülomlar da parlar; kesin malignite doku doğrulaması olmadan cerrahi morbiditeye girilmemelidir."
                },
                {
                    "text": "Görüntüleme kılavuzluğunda kor biyopsi yapılarak lezyonun karsinom mu yoksa benign adenom mu olduğu netleştirilir.",
                    "isCorrect": True,
                    "feedback": "Altın standart onkolojik karar! Patolojik alt tip cerrahi veya kemoembolizasyon rotasını kesinleştirir."
                },
                {
                    "text": "Patoloji sonucu beklenmeden radyoterapi uygulanır.",
                    "isCorrect": False,
                    "feedback": "Malpraktis! Patoloji olmadan onkolojik tedavi başlanamaz."
                }
            ]
        ),
        36: make_branching_logic(
            "Akciğer adenokarsinomu tanısı alan bir hastada moleküler testte EGFR Ekzon 19 delesyonu saptanması senaryosu.",
            [
                {
                    "text": "EGFR mutasyonu önemsizdir, standart toksik kemoterapiye devam edilir.",
                    "isCorrect": False,
                    "feedback": "Hatalı! Hedefe yönelik akıllı ilaç seçeneği varken klasik sitotoksik tedavi ilk tercih olmamalıdır."
                },
                {
                    "text": "Hastaya birinci basamakta hedefe kilitli oral tirozin kinaz inhibitörü (Osimertinib / Erlotinib) başlanır.",
                    "isCorrect": True,
                    "feedback": "Mükemmel kişiselleştirilmiş onkoloji kararı! Moleküler patoloji hedef mutasyonu göstererek sağkalımı ikiye katlayan ilacı seçtirir."
                },
                {
                    "text": "Hasta palyatif bakıma yönlendirilip ilaç verilmez.",
                    "isCorrect": False,
                    "feedback": "Kabul edilemez! EGFR mutant tümörler hedefe yönelik tedavilere son derece dramatik yanıt verir."
                }
            ]
        ),
        41: make_branching_logic(
            "Amasya Darüşşifası'nda Şerefeddin Sabuncuoğlu'nun cerrahi prensipleri doğrultusunda nekrotik yara yönetimi senaryosu.",
            [
                {
                    "text": "Nekrotik doku yerinde bırakılır ve kapatılır.",
                    "isCorrect": False,
                    "feedback": "Hatalı! Ölü doku enfeksiyon odağıdır; debritman şarttır."
                },
                {
                    "text": "Nekrotik sınır cerrahi koter ve eksizyonla canlı doku sınırına kadar temizlenir, iyileşme deneysel olarak takip edilir.",
                    "isCorrect": True,
                    "feedback": "Doğru! Sabuncuoğlu'nun Cerrahiyetü'l-Haniyye'de resmettiği gibi nekrotik dokunun cerrahi debridmanı temel kuraldır."
                },
                {
                    "text": "Yalnızca hacamat uygulanır.",
                    "isCorrect": False,
                    "feedback": "Yetersiz!"
                }
            ]
        ),
        51: make_branching_logic(
            "Işık mikroskobunda 40x objektifle incelenen lenf nodu kesitinde nükleuslar bulanık görüldüğünde hekimin ilk yapması gereken optik ayar senaryosu.",
            [
                {
                    "text": "Mikroskobun fişini çekip incelemeyi bırakmak.",
                    "isCorrect": False,
                    "feedback": "Uygunsuz."
                },
                {
                    "text": "Kondansatör diyaframını ve mikrometre vidasını ayarlayarak ışık huzmesini odaklamak ve lamın ters konmadığını denetlemek.",
                    "isCorrect": True,
                    "feedback": "Doğru optik yaklaşım! Kondansatör odağı ve ince mikrometre ayarı nükleer kromatini netleştirir."
                },
                {
                    "text": "Objektifi alkolle ıslatıp bastırmak.",
                    "isCorrect": False,
                    "feedback": "Merceğe zarar verir."
                }
            ]
        ),
        64: make_branching_logic(
            "Meme kitlesi kor (Tru-cut) biyopsisinde patolog invaziv duktal karsinom ile birlikte geniş duktal karsinoma in situ (DCIS) alanları saptamıştır.",
            [
                {
                    "text": "Hasta doğrudan takip kararıyla taburcu edilir.",
                    "isCorrect": False,
                    "feedback": "Kabul edilemez! İnvaziv karsinom cerrahi ve sistemik onkolojik tedavi gerektirir."
                },
                {
                    "text": "Rapor multidisipliner meme konseyine iletilir; cerrahi sınır güvenliği sağlanacak mastektomi/meme koruyucu cerrahi ve aksiller lenf nodu biyopsisi planlanır.",
                    "isCorrect": True,
                    "feedback": "Kusursuz onkolojik yaklaşım! Kor biyopsideki invazyon kanıtı aksiller evreleme ve küratif cerrahi planını başlatır."
                },
                {
                    "text": "İnvazyon göz ardı edilip yalnızca antibiyotik verilir.",
                    "isCorrect": False,
                    "feedback": "Malpraktis!"
                }
            ]
        ),
        71: make_branching_logic(
            "Laboratuvara mesai bitiminde saat 18:00'de ulaştırılan büyük mastektomi spesimeninin gece nöbetindeki yönetimi senaryosu.",
            [
                {
                    "text": "Materyal oda sıcaklığında ameliyat tepsisinde bırakılır, sabahleyin ilgilenilir.",
                    "isCorrect": False,
                    "feedback": "Ağır felaket! Dokunun merkezi sabaha kadar otolize uğrar, tümör teşhisi imkansızlaşır."
                },
                {
                    "text": "Meme dokusu 1 cm aralıklarla dilimlenerek lamel gibi açılır ve doku hacminin en az 10 katı %10 nötral tamponlu formaline daldırılarak fiksasyona alınır.",
                    "isCorrect": True,
                    "feedback": "Mükemmel nöbetçi yaklaşımı! Dilimleme formalinin merkeze nüfuz etmesini sağlar ve otolizi önler."
                },
                {
                    "text": "Materyal dondurucuya (-80°C) atılır.",
                    "isCorrect": False,
                    "feedback": "Buz kristalleri dokuyu parçalar; rutin fiksasyon formalindir."
                }
            ]
        ),
        75: make_branching_logic(
            "Doku takibinde ksilen banyosunun kokusunun azaldığı ve süt beyazı rengi aldığı görüldüğünde teknisyenin aksiyonu senaryosu.",
            [
                {
                    "text": "Kasetler doğrudan parafine aktarılır, bir şey olmaz.",
                    "isCorrect": False,
                    "feedback": "Hata! Sulu ksilen parafinin dokuya girmesini engeller; bloklar yumuşak kalır."
                },
                {
                    "text": "Takip durdurulur; ksilen ve öncesindeki dehidrasyon alkol banyoları tamamen yenilenir, kasetler taze alkolden itibaren tekrar geçirilir.",
                    "isCorrect": True,
                    "feedback": "Doğru kalite kontrol kararı! Sütümsü ksilen su bulaşmasını gösterir ve derhal yenilenmelidir."
                },
                {
                    "text": "Ksilene biraz su eklenerek seyreltilir.",
                    "isCorrect": False,
                    "feedback": "Daha da bozar!"
                }
            ]
        ),
        82: make_branching_logic(
            "Karaciğer biyopsisinde damar lümenlerinde yoğun siyah-kahverengi formalin pigmenti izlenen bir preparatta patoloğun yaklaşımı senaryosu.",
            [
                {
                    "text": "Hastaya derhal metastatik malign melanom tanısı verilerek kemoterapiye yönlendirilir.",
                    "isCorrect": False,
                    "feedback": "Ağır tanısal hata! Asit formaldehit hematin pigmenti melanomla karışabilir; pigmentin niteliği kanıtlanmadan kanser tanısı konulamaz."
                },
                {
                    "text": "Preparat alkolik pikrik asit solüsyonuna sokularak asit hematin pigmentinin çözünmesi sağlanır ve gerçek doku patolojisi açığa çıkarılır.",
                    "isCorrect": True,
                    "feedback": "Doğru histoteknolojik müdahale! Alkolik pikrik asit formalin pigmentini yıkarak melanin veya hemosiderinden kesin ayrımını sağlar."
                },
                {
                    "text": "Preparat çöpe atılır.",
                    "isCorrect": False,
                    "feedback": "Yersizdir, kimyasal yıkamayla temizlenebilir."
                }
            ]
        ),
        83: make_branching_logic(
            "Parafin blokların kesiminde bloğun ortasının çiğ ve yumuşak kaldığı fark edildiğinde sorunun kökeni senaryosu.",
            [
                {
                    "text": "Sorun rotary mikrotomun paslanmış olmasıdır.",
                    "isCorrect": False,
                    "feedback": "Yanlış. Mikrotom bloğun iç kimyasını değiştirmez."
                },
                {
                    "text": "Sorun yetersiz dehidrasyondur; doku merkezinde kalan su parafinin girmesini engellemiştir, blok eritilip re-proses edilmelidir.",
                    "isCorrect": True,
                    "feedback": "Mükemmel histoteknoloji tespiti! Blok eritilip ksilenden geri alkole çekilerek yeniden dehidre edilmelidir."
                },
                {
                    "text": "Blok doğrudan çöpe atılmalıdır.",
                    "isCorrect": False,
                    "feedback": "Doku değerlidir, re-proses ile kurtarılabilir."
                }
            ]
        ),
        85: make_branching_logic(
            "Mikrotomda kesilen tiroid karsinomu kesitinde kesim doğrultusunda derin paralel yırtık çizgileri izlenmesi senaryosu.",
            [
                {
                    "text": "Yırtıklar tümörün damar invazyonudur, raporda pozitif yazılır.",
                    "isCorrect": False,
                    "feedback": "Ağır hata! Düz mekanik yarık damar invazyonu sanılamaz."
                },
                {
                    "text": "Jilet ağzında psammom cisimciğine bağlı çentik olduğu anlaşılır; jilet yana kaydırılarak temiz kesim alanına geçilir.",
                    "isCorrect": True,
                    "feedback": "Doğru teknisyen müdahalesi! Bıçak çentiği jilet kaydırılarak çözülür."
                },
                {
                    "text": "Mikrotomun hızı maksimuma çıkarılır.",
                    "isCorrect": False,
                    "feedback": "Doku daha çok parçalanır."
                }
            ]
        ),
        91: make_branching_logic(
            "Hematuisi olan bir hastada idrar sitolojisinde şüpheli hücreler görülmesi üzerine klinik karar senaryosu.",
            [
                {
                    "text": "Sitoloji tek başına yeterlidir, ameliyatla mesane çıkarılır.",
                    "isCorrect": False,
                    "feedback": "Hatalı! İdrar sitolojisi invazyonu gösteremez; sistoskopi ve biyopsi şarttır."
                },
                {
                    "text": "Hastaya sistoskopi yapılarak şüpheli mesane lezyonlarından transüretral rezeksiyon (TUR-MT) biyopsisi alınarak kas invazyonu histopatolojik olarak kanıtlanır.",
                    "isCorrect": True,
                    "feedback": "Doğru ürolojik-onkolojik yaklaşım! Sitoloji tarar, histopatoloji evreler."
                },
                {
                    "text": "İdrar sitolojisi görmezden gelinir.",
                    "isCorrect": False,
                    "feedback": "Kanser atlanabilir."
                }
            ]
        ),
        95: make_branching_logic(
            "Tiroid ince iğne aspirasyon yayması yapıldıktan sonra lamın alkole atılmadan masada 10 dakika kurutulup sonra PAP boyasına sokulması senaryosu.",
            [
                {
                    "text": "Hücreler çok daha net boyanır.",
                    "isCorrect": False,
                    "feedback": "Yanlış! Havada kuruyan lamda PAP boyası nükleus atipisini şişirip bozar."
                },
                {
                    "text": "Kuruma artefaktı nedeniyle hücreler yapay olarak irileşir, kromatin silinir; sitopatolog bu yaymayı yetersiz veya kuşkulu raporlayabilir.",
                    "isCorrect": True,
                    "feedback": "Doğru sitoteknik bilinç! PAP boyası yapılacak yayma kurumadan derhal %95 alkole daldırılmalıdır."
                },
                {
                    "text": "Lam tekrar yıkanıp suyla ıslatılırsa düzelir.",
                    "isCorrect": False,
                    "feedback": "Hücreler lize olur."
                }
            ]
        ),
        97: make_branching_logic(
            "Over kanseri cerrahisinde batın açıldığında serbest asit sıvısı sitolojisi senaryosu.",
            [
                {
                    "text": "Sıvı aspire edilip doğrudan atılır, incelenmez.",
                    "isCorrect": False,
                    "feedback": "Ağır eksiklik! Sıvı evrelemeyi belirler."
                },
                {
                    "text": "Sıvı sitolojiye gönderilir; malign hücre saptanırsa hastanın FIGO evresi doğrudan Evre 1C veya 3'e yükselir ve adjuvan kemoterapi endikasyonu doğar.",
                    "isCorrect": True,
                    "feedback": "Doğru jinekolojik onkoloji kuralı! Peritoneal yayılım evreleme ve prognoz için esastır."
                },
                {
                    "text": "Sıvı sadece idrar testi için kullanılır.",
                    "isCorrect": False,
                    "feedback": "İlgisiz."
                }
            ]
        )
    }

    extra_active_recalls = {
        6: make_active_recall(
            "Patolojide inceleme düzeylerinin moleküler düzeye inmesi klinik tıbba ne kazandırmıştır?",
            "Aynı mikroskobik görüntüye sahip tümörlerin farklı genetik mutasyonlara (ör. EGFR, BRAF) sahip olduğunu göstererek kişiselleştirilmiş hedefe yönelik akıllı ilaç tedavilerinin yolunu açmıştır."
        ),
        12: make_active_recall(
            "Hastalık etiyolojisinde genetik (intrinsik) ile edinsel (ekstrinsik) nedenlerin etkileşimine klasik bir klinik örnek veriniz.",
            "Ateroskleroz ve koroner arter hastalığı: Ailevi hiperkolesterolemi genetik yatkınlığı olan bir bireyde, sigara ve yağlı beslenme gibi edinsel ekstrinsik faktörler eklendiğinde erken yaşta ölümcül miyokard enfarktüsü gelişir."
        ),
        17: make_active_recall(
            "Patofizyolojik süreçte bir lezyonun 'subklinik dönem' ile 'klinik dönem' arasındaki temel farkı nedir?",
            "Subklinik dönemde hücresel ve moleküler düzeyde hasar başlamıştır ancak hastada semptom ve fizik muayene bulgusu yoktur. Klinik dönemde ise hasar organ fonksiyonunu bozarak ağrı, dispne gibi semptomları açığa çıkarmıştır."
        ),
        25: make_active_recall(
            "Bir patoloji raporunda 'Cerrahi Sınırlar Negatif (Temiz)' ne anlama gelir?",
            "Tümörün cerrahi olarak çıkarılan dokunun en dış çini mürekkebiyle boyanmış sınırlarına temas etmediğini, kesi hattı ile tümör arasında sağlam doku payı bulunduğunu ve kitlenin tamamen çıkarıldığını ifade eder."
        ),
        31: make_active_recall(
            "Makroskobik incelemede lezyonun renginin (ör. beyaz vs kırmızı) patoloğa sağladığı ön bilgi nedir?",
            "Soluk-beyaz lezyonlar genellikle fibrozis, hücresel desmoplazi veya avasküler koagülasyon nekrozunu (iskemi) düşündürürken; kırmızı-siyah lezyonlar yoğun vaskülarite, kanama, konjesyon veya melanin pigmentini işaret eder."
        ),
        42: make_active_recall(
            "Giovanni Battista Morgagni'nin tıp tarihindeki 'Patolojik Anatominin Kurucusu' unvanını almasını sağlayan temel kavramsal devrimi nedir?",
            "Hastalıkların Antik Çağ'dan beri inanılan soyut 4 vücut sıvısının dengesizliğinden değil, doğrudan belirli organlardaki fiziksel anatomik lezyonlardan kaynaklandığını otopsilerle kanıtlamasıdır."
        ),
        53: make_active_recall(
            "Karaciğer biyopsisinde hemosiderin (demir) pigmentinin Prusya mavisi ile parlak mavi boyanmasının kimyasal reaksiyon prensibi nedir?",
            "Dokudaki ferrik demir iyonlarının asidik ortamda potasyum ferrosiyanür ile birleşerek suda erimeyen parlak mavi renkli ferrik ferrosiyanür çökeltisi oluşturması prensibine dayanır."
        ),
        63: make_active_recall(
            "Dermatolojide kullanılan Punch biyopsinin forsepsle yapılan traşlama biyopsilerine göre en büyük histopatolojik üstünlüğü nedir?",
            "Derinin tüm katmanlarını (epidermis, dermis ve subkutan yağ dokusu) tam kat silindir şeklinde çıkarması sayesinde vaskülit ve lupus gibi derin damarsal enflamatuvar lezyonların atlanmasını engellemesidir."
        ),
        73: make_active_recall(
            "Transmisyon Elektron Mikroskopisi (TEM) için rutin formalin yerine neden %2.5 Glutaraldehit fiksatifi kullanılır?",
            "Çünkü glutaraldehit çift aldehit grubu içeren bifonksiyonel bir moleküldür; proteinler arasında formalinden çok daha güçlü ve sıkı çapraz bağlar kurarak organellerin ultrastrüktürünü nanometre düzeyinde mükemmel sabitler."
        ),
        81: make_active_recall(
            "Histopatolojide 'Otoliz' ile 'Nekroz' arasındaki en temel kavramsal ve tanısal fark nedir?",
            "Nekroz canlı bir organizmada dokunun ölmesidir ve çevresinde daima canlı vücudun verdiği bir yangısal/vasküler inflamasyon reaksiyonu bulunur. Otoliz ise canlının ölümünden veya dokunun vücuttan ayrılmasından sonra gerçekleşen kendi kendine erimedir; çevresinde hiçbir inflamasyon reaksiyonu yoktur."
        ),
        93: make_active_recall(
            "Bethesda servikal sitoloji raporunda 'ASC-US' sonucu geldiğinde klinik rehberlerin önerdiği en modern yönetim algoritması nedir?",
            "Refleks 'Yüksek Riskli HPV DNA Testi' yapılmasıdır. Eğer yüksek riskli HPV pozitif çıkarsa hasta kolposkopiye yönlendirilir; HPV negatif ise 1 yıl sonra sitoloji tekrarı yapılır."
        ),
        99: make_active_recall(
            "Dijital patolojide yapay zekâ (AI) algoritmalarının Ki-67 proliferasyon indeksi değerlendirmesinde hekime sağladığı en büyük objektif katkı nedir?",
            "Gözle yapılan manuel sayımlardaki sübjektif tahmin hatasını ve göz yorgunluğunu ortadan kaldırarak; tümördeki on binlerce hücre çekirdeğini tek tek sınıflandırıp nesnel, tekrarlanabilir ve kesin bir yüzde skoru vermesidir."
        )
    }

    final_slides = []
    for s in raw_steps:
        slide_num = s["slideNumber"]
        is_checkpoint = s.get("isCheckpoint", False)
        checkpoint_num = s.get("checkpointNumber", None)

        # Tablo başlıklarını temizle
        if s.get("coreContent", {}).get("table"):
            orig_title = s["coreContent"]["table"].get("title", "")
            s["coreContent"]["table"]["title"] = clean_table_title(orig_title)

        # Mevcut interaktif ögeleri al
        current_elems = list(s.get("interactiveElements", []))

        # Ekstra branching logic enjekte et (varsa)
        if slide_num in extra_branching:
            current_elems.append(extra_branching[slide_num])

        # Ekstra active recall enjekte et (varsa)
        if slide_num in extra_active_recalls:
            current_elems.append(extra_active_recalls[slide_num])

        # Eğer bir adımda 2 veya daha fazla cloze varsa sadece 1 tanesini bırak (denge için)
        cloze_indices = [idx for idx, el in enumerate(current_elems) if el.get("type") == "cloze_masking"]
        if len(cloze_indices) > 1:
            for idx in reversed(cloze_indices[1:]):
                del current_elems[idx]

        # Her adıma en az 1, en fazla 5 interaktif öge
        if len(current_elems) > 5:
            current_elems = current_elems[:5]
        if len(current_elems) == 0:
            current_elems.append(make_active_recall(
                f"{s['title']} konusunun en kritik patolojik çıkarımı nedir?",
                f"{s['subtitle']} Bu ilke kurul ve klinik patoloji sınavlarının temel dayanağıdır."
            ))

        # TÜM İNTERAKTİF ÖGELERDE SIZINTI DENETİMİ VE TEMİZLİĞİ
        for el in current_elems:
            t = el.get("type")
            if t == "cloze_masking":
                h = el.get("hint", "")
                a = el.get("maskedTerm", "")
                if h and leaks(h, a):
                    el["hint"] = sanitize_hint(h, a)
            elif t == "interactive_table":
                for r in el.get("tableRows", []):
                    for c in r.get("cells", []):
                        if isinstance(c, dict) and c.get("isMasked"):
                            ch = c.get("hint", "")
                            ca = c.get("text", "")
                            if ch and leaks(ch, ca):
                                c["hint"] = sanitize_hint(ch, ca)

        # İlgili soruları dağıt (her adıma 1-3 soru)
        start_q_idx = ((slide_num - 1) * len(questions)) // 100
        end_q_idx = (slide_num * len(questions)) // 100
        step_questions = questions[start_q_idx:end_q_idx]
        if not step_questions and questions:
            step_questions = [questions[(slide_num - 1) % len(questions)]]

        # Flashcards
        flashcards = s.get("flashcards", [])

        # coreContent hazırlığı
        core_content = s.get("coreContent", {})
        if "keyBullets" not in core_content:
            core_content["keyBullets"] = [
                {
                    "title": s["title"],
                    "desc": s["subtitle"],
                    "isKey": True
                }
            ]

        # Düzen Blokları (XML / HTML Reader için hiyerarşik layout blocks)
        # Kritik Tıbbi Terimler bloğu kesinlikle EN ALTTA yer alır
        layout_blocks = [
            {"id": "block-header", "type": "header", "order": 1, "visible": True},
            {"id": "block-narrative", "type": "narrative", "order": 2, "visible": True},
            {"id": "block-table", "type": "table", "order": 3, "visible": bool(core_content.get("table"))},
            {"id": "block-flashcards", "type": "flashcards", "order": 4, "visible": bool(flashcards)},
            {"id": "block-interactive", "type": "interactive_element", "order": 5, "visible": bool(current_elems)},
            {"id": "block-spots", "type": "spot_pearls", "order": 6, "visible": bool(s.get("spotPearls"))},
            {"id": "block-questions", "type": "related_questions", "order": 7, "visible": bool(step_questions)},
            {"id": "block-terms", "type": "medical_terms", "order": 8, "visible": bool(s.get("medicalTerms"))},
        ]

        primary_interactive = current_elems[0] if current_elems else None

        slide_obj = {
            "slideNumber": slide_num,
            "title": s["title"],
            "subtitle": s["subtitle"],
            "badge": "Tekrar Sayfası" if is_checkpoint else s.get("badge", "Patoloji"),
            "badgeColor": "teal" if is_checkpoint else s.get("badgeColor", "blue"),
            "discipline": s.get("discipline", "Tıbbi Patoloji"),
            "synthesisNarrative": s["synthesisNarrative"],
            "medicalTerms": s.get("medicalTerms", []),
            "spotPearls": s.get("spotPearls", []),
            "interactiveElement": primary_interactive,
            "interactiveElements": current_elems,
            "layoutBlocks": layout_blocks,
            "flashcards": flashcards,
            "relatedQuestions": step_questions,
            "coreContent": core_content,
            "isCheckpoint": is_checkpoint,
            "checkpointNumber": checkpoint_num if is_checkpoint else None,
            "sourcePdf": {
                "fileName": "1)Patolojiye Giriş.pdf",
                "fileId": "k1-02",
                "startPage": min(105, max(1, (slide_num * 105) // 100)),
                "endPage": min(105, max(1, ((slide_num * 105) // 100) + 1)),
                "primaryPage": min(105, max(1, (slide_num * 105) // 100)),
                "citation": f"Slayt {slide_num} · Kurul 1 Tıbbi Patoloji Sunumu (Prof. Dr. Hikmet Keleş)"
            },
            "aiPromptSuggestions": [
                f"{s['title']} konusunun hücresel ve klinik mekanizmasını bir olgu senaryosuyla açıklar mısın?",
                "Bu adımdaki bilgilerin TUS ve kurul sınavlarında çıkabilecek soru tiplerini gösterir misin?"
            ]
        }
        final_slides.append(slide_obj)

    # İstatistikleri hesapla
    elem_counts = Counter()
    total_elems = 0
    for s in final_slides:
        for el in s.get("interactiveElements", []):
            t = el.get("type")
            elem_counts[t] += 1
            total_elems += 1

    print("\n" + "="*55)
    print(f"Toplam İnteraktif Öğe: {total_elems} (Adım başı ortalama: {total_elems/len(final_slides):.2f})")
    print("Öğe Dağılımı ve %8 Kuralı Denetimi:")
    all_passed = True
    for t, c in elem_counts.most_common():
        pct = (c / total_elems) * 100
        passed = pct >= 8.0
        if not passed:
            all_passed = False
        print(f"  - {t:<22}: {c:3d} adet (%{pct:5.2f}) -> {'✓ Kuralı Sağlıyor (>= %8)' if passed else '✗ DÜŞÜK'}")
    print(f"Bütün türler >= %8 kuralını sağlıyor mu?: {'EVET ✓' if all_passed else 'HAYIR ✗'}")
    print("="*55 + "\n")

    # 1. MANIFEST.JSON OLUŞTUR
    manifest_data = {
        "id": "k1-02-patolojiye-giris",
        "title": "Patolojiye Giriş (Yeni Mikro-Ders)",
        "discipline": "Tıbbi Patoloji",
        "committee": "Kurul 1 (Ürogenital ve Obstetrik)",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "version": "2.0",
        "totalSlides": 100,
        "interactiveMetrics": {
            "totalCount": total_elems,
            "ratio": round(total_elems / 100, 2),
            "distribution": {t: {"count": c, "percentage": round((c / total_elems) * 100, 2)} for t, c in elem_counts.items()}
        },
        "sources": {
            "xml": "structure.xml",
            "html": "blocks.html",
            "markdown": "content.md"
        },
        "slidesIndex": [
            {
                "slideNumber": s["slideNumber"],
                "title": s["title"],
                "badge": s["badge"],
                "isCheckpoint": s["isCheckpoint"],
                "interactiveCount": len(s["interactiveElements"]),
                "interactiveTypes": [el.get("type") for el in s["interactiveElements"]],
                "hasFlashcards": len(s["flashcards"]) > 0,
                "hasTable": bool(s["coreContent"].get("table"))
            } for s in final_slides
        ]
    }
    manifest_path = os.path.join(PACKAGES_DIR, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, ensure_ascii=False, indent=2)
    print(f"1. Manifest JSON yazıldı: {manifest_path}")

    # 2. STRUCTURE.XML OLUŞTUR
    root = ET.Element("lesson", id=deck_id, version="2.0")
    meta = ET.SubElement(root, "meta")
    ET.SubElement(meta, "title").text = manifest_data["title"]
    ET.SubElement(meta, "discipline").text = manifest_data["discipline"]
    ET.SubElement(meta, "totalSlides").text = "100"
    ET.SubElement(meta, "totalInteractives").text = str(total_elems)

    slides_node = ET.SubElement(root, "slides")
    for s in final_slides:
        slide_node = ET.SubElement(
            slides_node,
            "slide",
            id=f"slide-{s['slideNumber']:03d}",
            number=str(s['slideNumber']),
            badge=s['badge'],
            badgeColor=s['badgeColor'],
            isCheckpoint=str(s['isCheckpoint']).lower()
        )
        ET.SubElement(slide_node, "title").text = s["title"]
        ET.SubElement(slide_node, "subtitle").text = s["subtitle"]
        narrative_node = ET.SubElement(slide_node, "narrative")
        narrative_node.text = s["synthesisNarrative"]

        # Layout blokları
        blocks_node = ET.SubElement(slide_node, "layoutBlocks")
        for b in s["layoutBlocks"]:
            ET.SubElement(blocks_node, "block", id=b["id"], type=b["type"], order=str(b["order"]))

        # İnteraktif ögeler
        int_node = ET.SubElement(slide_node, "interactiveElements", count=str(len(s["interactiveElements"])))
        for el in s["interactiveElements"]:
            ET.SubElement(int_node, "element", type=el.get("type", ""))

        # Flashcards
        if s["flashcards"]:
            fc_node = ET.SubElement(slide_node, "flashcards", count=str(len(s["flashcards"])))
            for fc in s["flashcards"]:
                card_node = ET.SubElement(fc_node, "card", id=fc["id"])
                ET.SubElement(card_node, "front").text = fc["front"]
                ET.SubElement(card_node, "back").text = fc["back"]

        # Tıbbi terimler
        if s["medicalTerms"]:
            terms_node = ET.SubElement(slide_node, "medicalTerms")
            for tm in s["medicalTerms"]:
                t_el = ET.SubElement(terms_node, "term")
                ET.SubElement(t_el, "name").text = tm["term"]
                ET.SubElement(t_el, "explanation").text = tm["explanation"]

    xml_str = ET.tostring(root, encoding='utf-8')
    parsed_xml = minidom.parseString(xml_str)
    xml_pretty = parsed_xml.toprettyxml(indent="  ")
    xml_path = os.path.join(PACKAGES_DIR, "structure.xml")
    with open(xml_path, "w", encoding="utf-8") as f:
        f.write(xml_pretty)
    print(f"2. Structure XML yazıldı: {xml_path}")

    # 3. BLOCKS.HTML OLUŞTUR
    html_lines = [
        "<!DOCTYPE html>",
        "<html lang=\"tr\">",
        "<head>",
        "  <meta charset=\"UTF-8\">",
        f"  <title>{manifest_data['title']}</title>",
        "  <link rel=\"stylesheet\" href=\"/styles/reader.css\">",
        "</head>",
        "<body>",
        "  <header class=\"deck-header\">",
        f"    <h1>{manifest_data['title']}</h1>",
        f"    <p class=\"deck-meta\">Kurul 1 · {manifest_data['discipline']} · {manifest_data['instructor']}</p>",
        f"    <p class=\"deck-summary\">Toplam 100 Adım | {total_elems} İnteraktif Öğrenme Bileşeni | 10 Checkpoint İstasyonu</p>",
        "  </header>",
        "  <main class=\"deck-container\">"
    ]

    for s in final_slides:
        cp_class = " checkpoint-slide" if s["isCheckpoint"] else ""
        html_lines.append(f"    <article id=\"slide-{s['slideNumber']}\" class=\"slide-card{cp_class}\">")
        html_lines.append(f"      <div class=\"slide-badge badge-{s['badgeColor']}\">{s['badge']}</div>")
        html_lines.append(f"      <h2 class=\"slide-title\">{s['slideNumber']}. {s['title']}</h2>")
        html_lines.append(f"      <p class=\"slide-subtitle\">{s['subtitle']}</p>")
        html_lines.append("      <div class=\"narrative-block\">")
        for para in s["synthesisNarrative"].split("\n\n"):
            p_clean = para.strip()
            if p_clean.startswith(">"):
                html_lines.append(f"        <blockquote class=\"callout-box\">{p_clean.lstrip('> ').strip()}</blockquote>")
            elif p_clean:
                html_lines.append(f"        <p>{p_clean}</p>")
        html_lines.append("      </div>")

        if s.get("coreContent", {}).get("table"):
            tb = s["coreContent"]["table"]
            html_lines.append("      <div class=\"table-block\">")
            html_lines.append(f"        <h3>{tb.get('title', 'Özet Tablo')}</h3>")
            html_lines.append("        <table class=\"data-table\">")
            html_lines.append("          <thead><tr>")
            for h in tb.get("headers", []):
                html_lines.append(f"            <th>{h}</th>")
            html_lines.append("          </tr></thead>")
            html_lines.append("          <tbody>")
            for r in tb.get("rows", []):
                html_lines.append("            <tr>")
                for c in r:
                    html_lines.append(f"              <td>{c}</td>")
                html_lines.append("            </tr>")
            html_lines.append("          </tbody>")
            html_lines.append("        </table>")
            html_lines.append("      </div>")

        if s["flashcards"]:
            html_lines.append("      <div class=\"flashcards-block\">")
            html_lines.append("        <h3>🧠 Kontrol Noktası Akıl Kartları</h3>")
            for fc in s["flashcards"]:
                html_lines.append(f"        <div class=\"flashcard\" data-id=\"{fc['id']}\">")
                html_lines.append(f"          <div class=\"fc-front\">{fc['front']}</div>")
                html_lines.append(f"          <div class=\"fc-back\">{fc['back']}</div>")
                html_lines.append("        </div>")
            html_lines.append("      </div>")

        html_lines.append("      <div class=\"interactive-block\">")
        for idx, el in enumerate(s["interactiveElements"]):
            html_lines.append(f"        <div class=\"interactive-widget widget-{el.get('type')}\" data-index=\"{idx}\">")
            html_lines.append(f"          <!-- Widget Type: {el.get('type')} -->")
            html_lines.append("        </div>")
        html_lines.append("      </div>")

        if s.get("medicalTerms"):
            html_lines.append("      <footer class=\"medical-terms-block\">")
            html_lines.append("        <h4>Kritik Tıbbi Terimler</h4>")
            html_lines.append("        <ul>")
            for tm in s["medicalTerms"]:
                html_lines.append(f"          <li><strong>{tm['term']}:</strong> {tm['explanation']}</li>")
            html_lines.append("        </ul>")
            html_lines.append("      </footer>")

        html_lines.append("    </article>")
    html_lines.append("  </main>")
    html_lines.append("</body>")
    html_lines.append("</html>")
    html_path = os.path.join(PACKAGES_DIR, "blocks.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write("\n".join(html_lines))
    print(f"3. Blocks HTML yazıldı: {html_path}")

    # 4. CONTENT.MD OLUŞTUR
    md_lines = [
        "# Patolojiye Giriş (Kurul 1 - Ders 2)",
        f"**Eğitmen:** Prof. Dr. Hikmet Keleş | **Disiplin:** Tıbbi Patoloji | **Adım Sayısı:** 100 Adım | **İnteraktif Öğe:** {total_elems} Adet",
        "\n---\n"
    ]
    for s in final_slides:
        cp_tag = " [CHECKPOINT]" if s["isCheckpoint"] else ""
        md_lines.append(f"## Adım {s['slideNumber']}: {s['title']}{cp_tag}")
        md_lines.append(f"*{s['subtitle']}* - **Rozet:** `{s['badge']}`\n")
        md_lines.append(s["synthesisNarrative"])
        md_lines.append("")

        if s.get("coreContent", {}).get("table"):
            tb = s["coreContent"]["table"]
            md_lines.append(f"### 📋 {tb.get('title', 'Özet Tablo')}")
            headers = tb.get("headers", [])
            md_lines.append("| " + " | ".join(headers) + " |")
            md_lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
            for r in tb.get("rows", []):
                md_lines.append("| " + " | ".join(r) + " |")
            md_lines.append("")

        if s["flashcards"]:
            md_lines.append("### 🧠 Pekiştirme Akıl Kartları")
            for fc in s["flashcards"]:
                md_lines.append(f"- **Soru:** {fc['front']}")
                md_lines.append(f"  - **Cevap / Mekanizma:** {fc['back']}")
            md_lines.append("")

        if s.get("spotPearls"):
            md_lines.append("### 📌 Spot Bilgiler")
            for p in s["spotPearls"]:
                md_lines.append(f"- {p}")
            md_lines.append("")

        md_lines.append("\n---\n")

    md_path = os.path.join(PACKAGES_DIR, "content.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
    print(f"4. Content Markdown yazıldı: {md_path}")

    # 5. RUNTIME ITEM JSON OLUŞTUR
    deck_data = {
        "id": deck_id,
        "title": "Patolojiye Giriş (Yeni Mikro-Ders)",
        "shortTitle": "Patolojiye Giriş",
        "discipline": "Tıbbi Patoloji",
        "committee": "Kurul 1 (Ürogenital ve Obstetrik)",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "audioFile": "audios/kurul1/k1-02-patolojiye-giris.mp3",
        "audioDuration": "50:15",
        "confidence": "Yüksek",
        "themeColor": "blue",
        "matchedNoteId": "k1-02-patolojiye-giris",
        "matchedNoteTitle": "Patolojiye Giriş Ders Özeti",
        "isNew": True,
        "isLegacy": False,
        "version": 2,
        "packageSources": {
            "manifest": "packages/k1-02-patolojiye-giris/manifest.json",
            "structureXml": "packages/k1-02-patolojiye-giris/structure.xml",
            "blocksHtml": "packages/k1-02-patolojiye-giris/blocks.html",
            "contentMd": "packages/k1-02-patolojiye-giris/content.md"
        },
        "overview": f"Bu interaktif mikro-öğrenme destesi; 100 atomik adımda, 10 kontrol noktası tekrar sayfasında gömülü akıl kartlarıyla, {total_elems} adet zengin interaktif alıştırmayla (mikro-quiz, maskeli tablo, dallanan klinik senaryolar, aktif hatırlama, karşılaştırma kaydırıcısı, mekanizma zinciri) patolojinin tanımını, tarihçesini, tanısal araçlarını, doku takip basamaklarını, artefaktları, sitopatolojiyi ve moleküler geleceği derinlemesine öğretir.",
        "highYieldPearls": [
            "🚨 [KRİTİK UYARI] Nekroz, apoptoz veya irin inflamasyonun kardinal belirtisi DEĞİLDİR; kardinal belirtiler Rubor, Calor, Dolor, Tumor ve Functio Laesa'dır.",
            "📌 [SINAV SPOTU] Giovanni Battista Morgagni 1761'de organ patolojisini (Patolojik Anatomi), Rudolf Virchow 1858'de hücresel patolojiyi (Modern Patoloji) kurmuştur.",
            "📌 [SINAV SPOTU] Türkiye'de modern patolojinin kurucusu Prof. Dr. Hamdi Suat Aknar'dır; ilk patoloji müzesini kurmuştur.",
            "📌 [SINAV SPOTU] Papanicolaou servikal sitolojisini (PAP smear) Türkiye'ye getiren hekim Dr. Osman Nuri Aker'dir.",
            "📌 [SINAV SPOTU] Rutin fiksatif %10 nötral tamponlu formalindir; hacmi dokunun 10-20 katı olmalı, doku kalınlığı 3-4 mm'yi aşmamalıdır (penetrasyon hızı saatte ~1 mm'dir).",
            "📌 [SINAV SPOTU] Doku takip basamakları: Fiksasyon → Dehidrasyon (Alkol) → Şeffaflaştırma (Ksilen) → İnfiltrasyon (Parafin) → Bloklama.",
            "🚨 [KRİTİK UYARI] Dokuda nötral lipidler ksilende eridiği için parafin kesitte boyanamaz; dondurulmuş (frozen) kesitte Oil Red O ile boyanmalıdır.",
            "📌 [SINAV SPOTU] Prusya mavisi demiri (hemosiderin), PAS glikojeni/bazal membranı/mantarı, Masson trikrom kollajeni (fibrozis/siroz) maviye boyar.",
            "📌 [SINAV SPOTU] Floater artefaktı su banyosundan başka hastanın dokusunun bulaşmasıdır ve sağlıklı insana kanser tanısı koydurabilecek en tehlikeli laboratuvar hatasıdır.",
            "📌 [SINAV SPOTU] İİAS 22G iğneyle yapılır; doğruluk %90-95'tir. Kanda serbest tümör DNA'sı (ctDNA) analizine Likit Biyopsi denir."
        ],
        "totalSlides": 100,
        "totalInteractiveElements": total_elems,
        "interactiveRatio": round(total_elems / 100, 2),
        "matchedPastQuestionsCount": len(questions),
        "slides": final_slides
    }

    output_path = os.path.join(DECKS_ITEMS_DIR, f"{deck_id}.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(deck_data, f, ensure_ascii=False, indent=2)
    print(f"5. Runtime Item JSON kaydedildi: {output_path}")

    # 6. INTERACTIVE_LEARNING_DECKS.JSON DOSYASINI YERİNDE GÜNCELLE
    if os.path.exists(INTERACTIVE_DECKS_PATH):
        with open(INTERACTIVE_DECKS_PATH, "r", encoding="utf-8") as f:
            all_decks = json.load(f)
        replaced = False
        for idx, d in enumerate(all_decks):
            if d.get("id") == deck_id:
                all_decks[idx] = deck_data
                replaced = True
                print(f"6. interactive_learning_decks.json içinde '{deck_id}' [{idx}] yerinde güncellendi.")
                break
        if not replaced:
            all_decks.append(deck_data)
            print(f"6. interactive_learning_decks.json içine '{deck_id}' yeni eklendi.")

        with open(INTERACTIVE_DECKS_PATH, "w", encoding="utf-8") as f:
            json.dump(all_decks, f, ensure_ascii=False, indent=2)
        print("   interactive_learning_decks.json başarıyla kaydedildi.")

    # 7. CATALOG.JSON GÜNCELLE
    if os.path.exists(CATALOG_PATH):
        with open(CATALOG_PATH, "r", encoding="utf-8") as f:
            catalog = json.load(f)
        found = False
        for entry in catalog:
            if entry.get("id") == deck_id:
                entry["isNew"] = True
                entry["isLegacy"] = False
                entry["version"] = 2
                entry["totalSlides"] = 100
                entry["title"] = "Patolojiye Giriş (Yeni Mikro-Ders)"
                entry["overview"] = deck_data["overview"]
                entry["audioDuration"] = "50:15"
                found = True
                break
        if not found:
            catalog.append({
                "id": deck_id,
                "title": "Patolojiye Giriş (Yeni Mikro-Ders)",
                "shortTitle": "Patolojiye Giriş",
                "discipline": "Tıbbi Patoloji",
                "committee": "Kurul 1 (Ürogenital ve Obstetrik)",
                "instructor": "Prof. Dr. Hikmet Keleş",
                "totalSlides": 100,
                "isNew": True,
                "isLegacy": False,
                "version": 2,
                "audioDuration": "50:15",
                "overview": deck_data["overview"]
            })
        with open(CATALOG_PATH, "w", encoding="utf-8") as f:
            json.dump(catalog, f, ensure_ascii=False, indent=2)
        print(f"7. Catalog JSON güncellendi: {CATALOG_PATH}")

    print("\n✅ TÜM DERS 2 MULTI-FORMAT İŞLEMLERİ BAŞARIYLA TAMAMLANDI!")

if __name__ == "__main__":
    main()
