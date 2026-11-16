#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_full_lesson_4_deck.py
Kurul 1 - Ders 4: Hücre Hasarı ve Nekroz - I
Öğretim Üyesi: Prof. Dr. Hikmet Keleş

Yeni Nesil Multi-Format (JSON, XML, HTML, MD) Mikro-Öğrenme Motoru:
1. Tam 100 Atomik Adım.
2. 10 Özel Tekrar Sayfası (Checkpoints 1-10), her birinde 3'er adet gömülü Akıl Kartı (Flashcards, toplam 30 adet).
3. Kısa, yalın, gereksiz uzatmasız tablo başlıkları.
4. Tam dengeli 210-240 İnteraktif Öğe (Adım sayısının ~2.2 katı, [1.5x - 3.0x] aralığında).
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
PACKAGES_DIR = os.path.join(MEDS_ROOT, 'src', 'data', 'decks', 'packages', 'k1-04-hucre-hasari-ve-nekroz-i')
CATALOG_PATH = os.path.join(MEDS_ROOT, 'src', 'data', 'decks', 'catalog.json')
INTERACTIVE_DECKS_PATH = os.path.join(MEDS_ROOT, 'src', 'data', 'interactive_learning_decks.json')
ORNEK_SORULAR_PATH = os.path.join(MEDS_ROOT, 'src', 'data', 'ornek_sorular', 'k1', 'k1-04-hucre-hasari-ve-nekroz-i.json')

# Section importları
sys.path.insert(0, os.path.dirname(__file__))
from k1_04_deck_data import (
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
from k1_04_deck_data.helpers import (
    make_micro_quiz,
    make_interactive_table,
    make_cloze,
    make_before_after,
    make_causal_chain,
    make_active_recall,
    make_branching_logic,
    make_flashcard
)

# Sızıntı kontrol fonksiyonları
def fold(s):
    return str(s or '').lower().replace('ı', 'i').replace('İ', 'i')

def leaks(hint, answer):
    h = fold(hint)
    return any((w[:5] if len(w) > 5 else w) in h for w in re.findall(r'[\wçğıöşü%.,-]+', fold(answer)) if len(w) >= 3 or re.search(r'\d', w))

def sanitize_hint(hint, answer):
    if not hint or not leaks(hint, answer):
        return hint
    candidate_prompts = [
        "Klinik Kavram",
        "Tanısal İlke",
        "Temel Belirteç",
        "Uluslararası Terminoloji",
        "Patolojik Süreç",
        "Hücresel Mekanizma",
        "Kritik Bilgi"
    ]
    for p in candidate_prompts:
        if not leaks(p, answer):
            return p
    return "Temel Prensip"

def clean_table_title(title):
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

def build_extra_micro_quizzes():
    """15 ekstra mikro soru (micro_quiz) envanteri."""
    return {
        1: make_micro_quiz(
            "Biyolojik homeostazın bozulması ile karakterize olan hücre hasarının klinik pratikteki en temel anlamı nedir?",
            {
                "A": "Yalnızca yaşlı bireylerde görülen fizyolojik bir duraksamadır",
                "B": "Tüm edinsel ve organik hastalıkların ortak hücresel ve moleküler başlangıç noktasıdır",
                "C": "Hücrenin genetik yapısının tamamen kaybolmasıdır",
                "D": "Sadece bakteriyel enfeksiyonlarla tetiklenen bir tablodur",
                "E": "Daima geri dönüşsüz hücre ölümüyle sonuçlanan akut bir krizdir"
            },
            "B",
            {
                "A": "Hücre hasarı her yaşta ve her koşulda gelişebilir.",
                "B": "Doğru cevap B'dir: Bütün organik hastalıkların temelinde hücre hasarı yatar.",
                "C": "Genetik yapı hemen kaybolmaz.",
                "D": "İskemi, toksin, travma gibi birçok neden vardır.",
                "E": "Hafif hasar geri dönüşümlüdür."
            }
        ),
        3: make_micro_quiz(
            "Patolojide bir hastalığın gelişim basamaklarını tanımlarken 'etiyoloji' ile 'patogenez' arasındaki temel ayrım nasıldır?",
            {
                "A": "Etiyoloji sonuçtur, patogenez nedendir",
                "B": "Etiyoloji başlatıcı nedendir; patogenez ise nedenin tetiklediği hücresel ve moleküler mekanizma dizisidir",
                "C": "Her iki terim de eşanlamlıdır ve mikroskopik görüntüyü ifade eder",
                "D": "Patogenez sadece genetik mutasyonlarda kullanılır",
                "E": "Etiyoloji yalnızca fiziksel travmaları kapsar"
            },
            "B",
            {
                "A": "Tam tersidir; etiyoloji nedendir.",
                "B": "Doğru cevap B'dir: Etiyoloji başlatıcı faktör, patogenez ise hücresel gelişim mekanizmasıdır.",
                "C": "Eşanlamlı değildir.",
                "D": "Tüm hastalıklarda patogenez vardır.",
                "E": "Tüm nedenleri kapsar."
            }
        ),
        5: make_micro_quiz(
            "İskeminin saf hipoksiye kıyasla dokuları çok daha hızlı ve şiddetli şekilde nekroza sürüklemesinin temel patofizyolojik nedeni nedir?",
            {
                "A": "İskemide kan akımı kesildiği için hem oksijen hem glukoz kesilir ve laktik asit dokuda birikir",
                "B": "Hipokside kan akımı tamamen durmuştur",
                "C": "İskemide hücre içine sodyum girişi olmaz",
                "D": "Hipoksi sadece kalbi etkilerken iskemi tüm organları etkiler",
                "E": "İskemide hücre zarı ilk saniyede parçalanır"
            },
            "A",
            {
                "A": "Doğru cevap A'dır: İskemide perfüzyon durduğu için anaerobik glikolitik substrat (glukoz) da gelemez ve asit atıklar birikir.",
                "B": "Hipokside perfüzyon devam edebilir.",
                "C": "Sodyum girişi her ikisinde de olur.",
                "D": "Tüm dokularda geçerlidir.",
                "E": "Zar hemen parçalanmaz."
            }
        ),
        7: make_micro_quiz(
            "Karbon tetraklorür (CCl4) maruziyetinde hepatositlerde lipid peroksidasyonunu başlatan reaktif serbest radikal nerede ve hangi enzimle üretilir?",
            {
                "A": "Mitokondri iç zarında ATP sentaz ile",
                "B": "Düz endoplazmik retikulumda Sitokrom P-450 enzimi ile (CCl3*)",
                "C": "Lizozom içinde asit hidrolaz ile",
                "D": "Çekirdekte DNA polimeraz ile",
                "E": "Peroksizomda katalaz enzimi ile"
            },
            "B",
            {
                "A": "Mitokondride üretilmez.",
                "B": "Doğru cevap B'dir: Karaciğer düz ER'sinde CYP2E1 (sitokrom P-450) ile CCl3* radikaline dönüştürülür.",
                "C": "Lizozomda üretilmez.",
                "D": "Nükleer enzim değildir.",
                "E": "Katalaz koruyucu enzimdir."
            }
        ),
        10: make_micro_quiz(
            "Endoplazmik retikulum lümeninde katlanamamış hatalı proteinlerin birikmesi hücrede hangi patolojik stres yanıtını tetikleyerek apoptoza yol açar?",
            {
                "A": "Mitokondriyal krista lizisi",
                "B": "ER Stresi ve katlanmamış protein yanıtı (UPR)",
                "C": "Lizozomal aşırı yüklenme sendromu",
                "D": "Golgi vezikül agregasyonu",
                "E": "Peroksizomal oksidatif fırtına"
            },
            "B",
            {
                "A": "Mitokondriyal primer olay değildir.",
                "B": "Doğru cevap B'dir: Hatalı katlanan proteinler ER stresini ve UPR yolağını aktive ederek kaspazları tetikler.",
                "C": "Lizozomal depo hastalığı değildir.",
                "D": "Golgi primer tetikleyici değildir.",
                "E": "Peroksizom ilişkisizdir."
            }
        ),
        12: make_micro_quiz(
            "İyonizan radyasyonun dokularda DNA çift zincir kırıkları oluşturmasında en etkili olan reaktif serbest radikal türü hangisidir?",
            {
                "A": "Süperoksit anyonu (O2*-)",
                "B": "Hidroksil radikali (OH*)",
                "C": "Hidrojen peroksit (H2O2)",
                "D": "Nitrik oksit (NO)",
                "E": "Hipokloröz asit (HOCl)"
            },
            "B",
            {
                "A": "Süperoksit daha zayıf radikaldir.",
                "B": "Doğru cevap B'dir: Suyun radyoliziyle oluşan hidroksil radikali en reaktif ve yıkıcı DNA hasarlayıcıdır.",
                "C": "H2O2 serbest radikal değildir, zayıf oksitleyicidir.",
                "D": "NO vazodilatatördür.",
                "E": "HOCl nötrofillerin ürettiği bileşiktir."
            }
        ),
        17: make_micro_quiz(
            "Geri dönüşümlü hücre hasarını geri dönüşümsüz hücre hasarından (nekroz) ayıran en temel hücresel bariyer özelliği nedir?",
            {
                "A": "Ribozomların çekirdeğe girmesi",
                "B": "Plazma ve organel membran bütünlüğünün korunmuş olması",
                "C": "Hücre içi kalsiyumun sıfırlanması",
                "D": "ATP üretiminin tamamen durması",
                "E": "Sitoplazmada nükleus oluşması"
            },
            "B",
            {
                "A": "Ribozomlar çekirdeğe girmez.",
                "B": "Doğru cevap B'dir: Membran sağlam kaldığı sürece hasar geri dönüşümlüdür; membran delindiğinde nekroz kaçınılmazdır.",
                "C": "Kalsiyum sıfırlanmaz.",
                "D": "ATP tamamen durmaz, azalır.",
                "E": "Biyolojik olarak olanaksızdır."
            }
        ),
        20: make_micro_quiz(
            "Hücresel şişme (hidropik değişim) gösteren bir hücrede ışık mikroskobunda izlenen berrak vakuoller hangi organelin genişlemesine karşılık gelir?",
            {
                "A": "Lizozomların",
                "B": "Genişlemiş endoplazmik retikulum sisternalarının",
                "C": "Mitokondri matriksinin",
                "D": "Golgi cisimciğinin",
                "E": "Nükleolusun"
            },
            "B",
            {
                "A": "Lizozomlar berrak vakuol oluşturmaz.",
                "B": "Doğru cevap B'dir: Endoplazmik retikulum su toplayarak genişler ve optik olarak boş berrak vakuoller oluşturur.",
                "C": "Mitokondri küçük kalır.",
                "D": "Golgi ana vakuol kaynağı değildir.",
                "E": "Nükleolus çekirdektedir."
            }
        ),
        22: make_micro_quiz(
            "Geri dönüşümlü hasarda protein sentezinin hızla düşmesine yol açan ultrastrüktürel (elektron mikroskobik) değişiklik hangisidir?",
            {
                "A": "Plazma zarında bleb oluşumu",
                "B": "Ribozomların granüllü endoplazmik retikulumdan ayrılması (detachment)",
                "C": "Mitokondri kristalarının çoğalması",
                "D": "Nükleer membranın erimesi",
                "E": "Miyelin figürlerinin lizozomu tıkaması"
            },
            "B",
            {
                "A": "Blebler membranözdür, protein sentezlemez.",
                "B": "Doğru cevap B'dir: Sisternal dilatasyon ribozomları GER'den koparır ve translasyon durur.",
                "C": "Kristalar çoğalmaz.",
                "D": "Nükleer membran geri dönüşümlüde erimez.",
                "E": "Miyelin figürleri membran fosfolipididir."
            }
        ),
        24: make_micro_quiz(
            "Parankimatöz hücrelerde nötral trigliseritlerin anormal birikimiyle karakterize olan ikinci temel geri dönüşümlü hasar formu hangisidir?",
            {
                "A": "Amiloidoz",
                "B": "Steatoz (Yağlanma)",
                "C": "Mukoid dejenerasyon",
                "D": "Glikojenoz",
                "E": "Hemosideroz"
            },
            "B",
            {
                "A": "Amiloidoz protein birikimidir.",
                "B": "Doğru cevap B'dir: Steatoz parankim hücrelerinde trigliserit birikimidir ve geri dönüşümlüdür.",
                "C": "Mukoid birikim bağ dokusundadır.",
                "D": "Glikojenoz glikojen depo hastalığıdır.",
                "E": "Hemosideroz demir birikimidir."
            }
        ),
        26: make_micro_quiz(
            "Kronik derin anemisi olan bir hastada kalp kasında izlenen ardışık sarı ve kırmızı şeritlerin oluşturduğu makroskobik görünüme ne ad verilir?",
            {
                "A": "Kırmızı nöron kalbi",
                "B": "Kaplan derisi kalp (Cor tigrinum)",
                "C": "Zırhlı kalp (Cor bovinum)",
                "D": "Kahverengi kalp atrofisi",
                "E": "Romatizmal ekmek-tereyağı kalbi"
            },
            "B",
            {
                "A": "Kırmızı nöron beyindedir.",
                "B": "Doğru cevap B'dir: Hipoksik yağlanmanın miyokarddaki çizgili paternine Cor Tigrinum denir.",
                "C": "Cor bovinum masif hipertrofidir.",
                "D": "Kahverengi atrofi lipofuskin birikimidir.",
                "E": "Ekmek-tereyağı fibrinöz perikardittir."
            }
        ),
        30: make_micro_quiz(
            "Patolojide hücrenin geri dönüşümlü hasar evresinden kaçınılmaz ölüme geçtiği kritik biyokimyasal sınıra ne ad verilir?",
            {
                "A": "Hayflick limiti",
                "B": "Geri dönüşü olmayan nokta (The point of no return)",
                "C": "Mitotik arrest sınırı",
                "D": "Apoptotik eşik penceresi",
                "E": "Kompensatuvar plato"
            },
            "B",
            {
                "A": "Hayflick replikatif yaşlanmadır.",
                "B": "Doğru cevap B'dir: Point of no return geri dönüşsüzlüğe geçilen eşiktir.",
                "C": "Hücre bölünmesiyle ilgisizdir.",
                "D": "Nekroz eşiğidir.",
                "E": "Adaptasyon terimidir."
            }
        ),
        36: make_micro_quiz(
            "Ağır ve onarılamaz DNA hasarı saptandığında hücre döngüsünü durduran ve hücreyi apoptoza yönlendiren 'genomun bekçisi' tümör baskılayıcı protein hangisidir?",
            {
                "A": "K-Ras",
                "B": "p53",
                "C": "Bcl-2",
                "D": "HER2/neu",
                "E": "SIRT1"
            },
            "B",
            {
                "A": "K-Ras onkogendir.",
                "B": "Doğru cevap B'dir: p53 DNA hasarında tamir veya apoptoz kararı veren ana tümör baskılayıcıdır.",
                "C": "Bcl-2 anti-apoptotiktir.",
                "D": "HER2 büyüme faktörü reseptörüdür.",
                "E": "SIRT1 deasetilazdır."
            }
        ),
        40: make_micro_quiz(
            "Nekroz ile apoptoz karşılaştırıldığında aşağıdakilerden hangisi YALNIZCA nekroz için geçerli bir özelliktir?",
            {
                "A": "Hücre zarlarının parçalanması ve çevre dokuda yoğun inflamasyon oluşması",
                "B": "Hücrenin büzüşerek apoptotik cisimcikler oluşturması",
                "C": "Fizyolojik embriyogenez süreçlerinde de rol oynaması",
                "D": "Kaspaz enzimlerinin aktif olarak çalışması",
                "E": "Hücre zarı bütünlüğünün korunması"
            },
            "A",
            {
                "A": "Doğru cevap A'dır: Membran parçalanması ve inflamasyon nekrozun değişmez damgasıdır.",
                "B": "Apoptoza aittir.",
                "C": "Apoptoza aittir; nekroz daima patolojiktir.",
                "D": "Kaspazlar apoptozda çalışır.",
                "E": "Zar korunması apoptoza aittir."
            }
        ),
        50: make_micro_quiz(
            "Nekroza uğrayan hücrelerin sitoplazmasının canlı hücrelere göre çok daha koyu pembe-kırmızı (artmış eozinofili) boyanmasının 2 temel nedeni nedir?",
            {
                "A": "Glikojen artışı ve DNA çoğalması",
                "B": "Denatüre proteinlerin eozini fazla bağlaması ve bazofilik RNA'nın kaybı",
                "C": "Lipid damlacıklarının boyayı emmesi ve kalsiyum azalması",
                "D": "Mitokondrilerin bölünmesi ve nükleus irileşmesi",
                "E": "Miyelin figürlerinin asit salgılaması"
            },
            "B",
            {
                "A": "Glikojen tükenir.",
                "B": "Doğru cevap B'dir: Protein pıhtılaşması eozini çeker; ribonükleazlarla RNA parçalanması mavi rengi siler.",
                "C": "Lipidler boyanmaz boş kalır.",
                "D": "Mitokondriler bölünmez, şişer.",
                "E": "Miyelin boyanmayı açıklamaz."
            }
        )
    }

def build_extra_branching_logic():
    """17 ekstra dallanan klinik karar senaryosu (branching_logic)."""
    return {
        11: make_branching_logic(
            "Ağır protein malnütrisyonu (Kwaşiorkor) gelişen 3 yaşındaki çocukta karaciğer biyopsisinde izlenen steatoz mekanizması senaryosu.",
            [
                {
                    "text": "Çocuk aşırı yağlı hamburger yediği için karaciğer yağlanmıştır.",
                    "isCorrect": False,
                    "feedback": "Hatalı! Çocuk açtır ve protein alamamaktadır."
                },
                {
                    "text": "Diyette aminoasit olmadığı için apoprotein sentezlenemez; trigliseritler VLDL olarak karaciğerden atılamaz ve hepatositte birikir.",
                    "isCorrect": True,
                    "feedback": "Kusursuz patobiyokimyasal açıklama! Apoprotein yokluğu lipitlerin karaciğerde hapsolmasına yol açar."
                },
                {
                    "text": "Karaciğer hücreleri bölünerek yağ hücresine dönüşmüştür.",
                    "isCorrect": False,
                    "feedback": "Biyolojik olarak imkansızdır."
                }
            ]
        ),
        21: make_branching_logic(
            "Ağır septik şokta olan hastada böbreğin makroskobik olarak belirgin soluk ve gergin görünmesinin nedeni senaryosu.",
            [
                {
                    "text": "Hastada kan kalmamış, tüm eritrositler buharlaşmıştır.",
                    "isCorrect": False,
                    "feedback": "Tıbbi olarak anlamsızdır."
                },
                {
                    "text": "İskemik tübül epitel hücreleri Na+/K+ pompası durduğu için su toplayıp şişmiş; komşu kapiller damarları dıştan ezerek dokuyu kansızlaştırmıştır.",
                    "isCorrect": True,
                    "feedback": "Doğru patolojik mekanizma! Şişen parankim hücreleri mikrosirkülasyonu sıkıştırarak organı soluklaştırır."
                },
                {
                    "text": "Böbrek kalsiyum taşıyla kaplanmıştır.",
                    "isCorrect": False,
                    "feedback": "İlgisiz."
                }
            ]
        ),
        25: make_branching_logic(
            "Kronik alkol bağımlısı bir hastada karaciğer biyopsisinde çekirdeği kenara iten tek dev yağ damlası saptandığında lezyonun niteliği senaryosu.",
            [
                {
                    "text": "Geri dönüşümsüz malign liposarkomdur, kemoterapi şarttır.",
                    "isCorrect": False,
                    "feedback": "Ağır tanısal hata! Bu selim ve geri dönüşümlü bir steatozdur."
                },
                {
                    "text": "Geri dönüşümlü makroveziküler steatozdur; hasta alkolü bırakırsa karaciğer haftalar içinde tamamen normale dönebilir.",
                    "isCorrect": True,
                    "feedback": "Doğru patoloji yaklaşımı! Steatoz hücre zarları sağlam kaldığı sürece tamamen geri dönüşümlüdür."
                },
                {
                    "text": "Hemen karaciğer nakli yapılmalıdır.",
                    "isCorrect": False,
                    "feedback": "Yersizdir, detoksifikasyonla düzelir."
                }
            ]
        ),
        31: make_branching_logic(
            "Elektron mikroskobunda mitokondri matriksinde elektron-yoğun amorf kalsiyum birikintileri saptanan bir dokunun klinik prognozu senaryosu.",
            [
                {
                    "text": "Doku geri dönüşümlü evrededir; oksijen verilirse tamamen iyileşir.",
                    "isCorrect": False,
                    "feedback": "Hatalı! Amorf kalsiyum birikintileri geri dönüşümsüz hasarın kesin kanıtıdır."
                },
                {
                    "text": "Doku 'point of no return'ü aşmış, geri dönüşümsüz nekroza girmiştir; hücreler artık kurtarılamaz.",
                    "isCorrect": True,
                    "feedback": "Mükemmel ultrastrüktürel yorum! Amorf kalsiyum agregatları mitokondrinin öldüğünü belgeler."
                },
                {
                    "text": "Hücreler apoptoza değil hipertrofiye gidecektir.",
                    "isCorrect": False,
                    "feedback": "Yanlış."
                }
            ]
        ),
        33: make_branching_logic(
            "İskemik dokuda lizozomal enzimlerin sitoplazmada bu kadar hızlı ve yıkıcı organel sindirimi (otoliz) yapabilmesinin nedeni senaryosu.",
            [
                {
                    "text": "Hücre içinin aşırı alkali olması enzimlerin çalışmasını sağlar.",
                    "isCorrect": False,
                    "feedback": "Yanlış! İskemide pH asidik olur."
                },
                {
                    "text": "Anaerobik glikolizle biriken laktik asidin hücre içi pH'ı düşürmesi, asit hidrolazların maksimum aktiviteyle çalışmasına zemin hazırlar.",
                    "isCorrect": True,
                    "feedback": "Doğru biyokimyasal kavrayış! Düşük pH lizozomal asit enzimlerinin doğal çalışma sahasıdır."
                },
                {
                    "text": "Lizozomlar hücre dışından enzim çeker.",
                    "isCorrect": False,
                    "feedback": "Otoliz iç enzimlerle olur."
                }
            ]
        ),
        37: make_branching_logic(
            "Göğüs ağrısı olan hastada kanda Troponin I pozitif saptandığında klinisyenin patolojik çıkarımı senaryosu.",
            [
                {
                    "text": "Miyosit zarları tamamen sağlamdır, yalnızca geçici spazm vardır.",
                    "isCorrect": False,
                    "feedback": "Hatalı! Zar sağlamken troponin kana geçemez."
                },
                {
                    "text": "Miyokard hücre membranları yırtılmış, sitoplazmik içerik kana dökülmüş ve geri dönüşümsüz nekroz başlamıştır.",
                    "isCorrect": True,
                    "feedback": "Kusursuz klinik patoloji tespiti! Troponin salınımı membran bütünlüğünün bozulduğunu ve nekrozu kanıtlar."
                },
                {
                    "text": "Hasta sadece grip olmuştur.",
                    "isCorrect": False,
                    "feedback": "Kabul edilemez!"
                }
            ]
        ),
        41: make_branching_logic(
            "Otopsi yapılan bir cesette organ erimesi ile canlı insanda gelişen bacak nekrozu arasındaki ayrım senaryosu.",
            [
                {
                    "text": "Her iki durumda da çevre dokularda yoğun nötrofilik infiltrasyon vardır.",
                    "isCorrect": False,
                    "feedback": "Hatalı! Ölü cesette inflamasyon yanıtı oluşamaz."
                },
                {
                    "text": "Canlıdaki nekrozda çevre sağlam doku damarsal ve hücresel inflamasyon (marjinal hiperemi, nötrofil) verir; cesetteki otolizde ise inflamasyon sıfırdır.",
                    "isCorrect": True,
                    "feedback": "Mükemmel adli patoloji ilkesi! Nekroz canlı dokuda gerçekleşir ve inflamasyon içerir; postmortem otoliz steril ve inflamasyonsuzdur."
                },
                {
                    "text": "İki tablo arasında hiçbir fark yoktur.",
                    "isCorrect": False,
                    "feedback": "Yanlış."
                }
            ]
        ),
        44: make_branching_logic(
            "Böbrek enfarktüsünde ışık mikroskobunda glomerül ve tübül sınırlarının seçilebildiği ancak hiçbir çekirdeğin boyanmadığı tablonun adı senaryosu.",
            [
                {
                    "text": "Sıvılaşma nekrozudur, doku tamamen erimiştir.",
                    "isCorrect": False,
                    "feedback": "Yanlış! Sıvılaşmada konturlar korunamaz."
                },
                {
                    "text": "Koagülatif nekrozdur; protein denatürasyonu doku mimarisini korumuş, 'hayalet hücreler' oluşmuştur.",
                    "isCorrect": True,
                    "feedback": "Doğru histopatolojik teşhis! Hayalet hücreler koagülatif nekrozun damgasıdır."
                },
                {
                    "text": "Fizyolojik apoptoz kavitasyonudur.",
                    "isCorrect": False,
                    "feedback": "Alakasız."
                }
            ]
        ),
        51: make_branching_logic(
            "Karaciğer nekrozunda sitoplazmanın camsı homojen görünüm almasının PAS boyası ile teyidi senaryosu.",
            [
                {
                    "text": "Nekrotik hücreler glikojen depoladığı için PAS ile kapkara boyanır.",
                    "isCorrect": False,
                    "feedback": "Hatalı! Nekrotik hücrede glikojen tükenmiştir."
                },
                {
                    "text": "İskemik glikoliz glikojen granüllerini tükettiği için nekrotik alan PAS boyası tutmaz ve camsı kalır.",
                    "isCorrect": True,
                    "feedback": "Doğru histokimyasal mantık! Glikojen kaybı camsı homojenliğin biyokimyasal nedenidir."
                },
                {
                    "text": "PAS boyası yalnızca kemikleri boyar.",
                    "isCorrect": False,
                    "feedback": "Yanlış."
                }
            ]
        ),
        55: make_branching_logic(
            "Doku kesitinde koyu pembe sitoplazmalı ve güve yeniği delikleri olan hücrelerin çekirdek incelemesi senaryosu.",
            [
                {
                    "text": "Çekirdekler tamamen normal boyuttadır ve aktif mitoz göstermektedir.",
                    "isCorrect": False,
                    "feedback": "Hatalı! Nekrotik hücre bölünemez."
                },
                {
                    "text": "Çekirdekler piknozla büzülmüş, karyoreksisle parçalanmış veya karyolizisle tamamen silinmiştir.",
                    "isCorrect": True,
                    "feedback": "Mükemmel tanısal bütünlük! Nekrotik sitoplazmaya nükleer piknoz/karyolizis eşlik eder."
                },
                {
                    "text": "Hücrelerin çekirdeği ikiye katlanmıştır.",
                    "isCorrect": False,
                    "feedback": "Yanlış."
                }
            ]
        ),
        57: make_branching_logic(
            "Mikroskopta nükleusun su kaybedip büzülerek küçük, kapkara bir mürekkep damlasına dönüştüğü evrenin adı senaryosu.",
            [
                {
                    "text": "Karyolizis",
                    "isCorrect": False,
                    "feedback": "Yanlış! Karyolizis çekirdeğin eriyip solmasıdır."
                },
                {
                    "text": "Piknoz (Pyknosis)",
                    "isCorrect": True,
                    "feedback": "Doğru nükleer evre! Piknoz nükleer büzülme ve aşırı bazofilidir."
                },
                {
                    "text": "Karyoreksis",
                    "isCorrect": False,
                    "feedback": "Karyoreksis parçalanmadır."
                }
            ]
        ),
        60: make_branching_logic(
            "DNAaz enzimlerinin nükleer kromatini eritmesi sonucu çekirdeğin mikroskopta tamamen görünmez hale geldiği evre senaryosu.",
            [
                {
                    "text": "Karyolizis (Karyolysis)",
                    "isCorrect": True,
                    "feedback": "Kusursuz nükleer tanı! Karyolizis nükleusun lizisle tamamen silinmesidir."
                },
                {
                    "text": "Piknoz",
                    "isCorrect": False,
                    "feedback": "Piknozda çekirdek vardır ve kapkaradır."
                },
                {
                    "text": "Mitoz",
                    "isCorrect": False,
                    "feedback": "İlgisiz."
                }
            ]
        ),
        66: make_branching_logic(
            "Akciğerde pulmoner emboli sonucu gelişen enfarktüsün neden soluk değil de kırmızı (hemorajik) olduğu senaryosu.",
            [
                {
                    "text": "Akciğer katı bir organ olduğu için kan sızamaz.",
                    "isCorrect": False,
                    "feedback": "Yanlış! Akciğer gevşek dokudur."
                },
                {
                    "text": "Akciğer çift dolaşıma (pulmoner arter + bronşiyal arter) ve süngerimsi gevşek dokuya sahiptir; iskemik alana komşu damarlardan kan sızarak nekrozu kırmızıya boyar.",
                    "isCorrect": True,
                    "feedback": "Doğru organ patolojisi kuralı! Çift dolaşım ve gevşek doku kırmızı enfarktüs nedenidir."
                },
                {
                    "text": "Akciğer enfarktüsü daima tüberkülozdur.",
                    "isCorrect": False,
                    "feedback": "Hatalı."
                }
            ]
        ),
        70: make_branching_logic(
            "Karaciğerinde 5 cm çapında fluktuasyon veren piyojenik apse saptanan hastada doku nekrozunun kalıbı senaryosu.",
            [
                {
                    "text": "Koagülatif nekrozdur, doku pişmiş et gibi sert kalacaktır.",
                    "isCorrect": False,
                    "feedback": "Yanlış! Bakteriyel apseler sıvılaşma nekrozudur."
                },
                {
                    "text": "Sıvılaşma (likefaksiyon) nekrozudur; nötrofil enzimleri dokuyu eriterek viskoz püy kitlesine çevirmiştir.",
                    "isCorrect": True,
                    "feedback": "Doğru patoloji tanısı! Piyojenik bakteriler sıvılaşma nekrozu ve püy oluşturur."
                },
                {
                    "text": "Kazeöz nekrozdur, sadece kireçlenir.",
                    "isCorrect": False,
                    "feedback": "Kazeöz tüberkülozdadır."
                }
            ]
        ),
        74: make_branching_logic(
            "İnme geçiren 70 yaşındaki hastanın beyninde ilk 18 saatte izlenen eozinofilik büzük nöronların klinik adı senaryosu.",
            [
                {
                    "text": "Kırmızı nöron (Red neuron)",
                    "isCorrect": True,
                    "feedback": "Doğru nöropatoloji bilgisi! Akut serebral iskeminin erken patognomonik hücresi kırmızı nörondur."
                },
                {
                    "text": "Psammom cisimciği",
                    "isCorrect": False,
                    "feedback": "Psammom kalsifikasyondur."
                },
                {
                    "text": "Lewy cisimciği",
                    "isCorrect": False,
                    "feedback": "Lewy Parkinson'dadır."
                }
            ]
        ),
        80: make_branching_logic(
            "Periferik arter hastalığı olan hastanın ayak başparmağının kararıp kuruduğu, ağrısız mumyalaştığı ve kötü koku olmadığı senaryo.",
            [
                {
                    "text": "Tablo kuru gangrendir; steril bir koagülatif nekrozdur ve demarkasyon hattı olgunlaşınca elektif cerrahi planlanabilir.",
                    "isCorrect": True,
                    "feedback": "Mükemmel cerrahi patoloji kararı! Kuru gangrende enfeksiyon yoktur, hasta acil sepsiste değildir."
                },
                {
                    "text": "Acil gazlı gangrendir, bacak hemen ampute edilmelidir.",
                    "isCorrect": False,
                    "feedback": "Yanlış! Gaz ve krepitasyon yoktur."
                },
                {
                    "text": "Ayak parmağı yıkanınca canlı pembe rengine dönecektir.",
                    "isCorrect": False,
                    "feedback": "Nekroz geri dönmez."
                }
            ]
        ),
        84: make_branching_logic(
            "Diyabetik hastanın ayağındaki yaranın kötü kokulu püy saldığı, sınırının hızla bacağa tırmandığı ve hastanın ateşlendiği senaryo.",
            [
                {
                    "text": "Islak gangrendir; sekonder bakteriyel sıvılaşma nekrozu ve sepsis tehlikesi vardır, acil cerrahi amputasyon şarttır.",
                    "isCorrect": True,
                    "feedback": "Hayat kurtarıcı cerrahi yaklaşım! Islak gangrende demarkasyon hattı beklenmez, acil amputasyon gerekir."
                },
                {
                    "text": "Kuru gangrendir, hiçbir şey yapılmamalıdır.",
                    "isCorrect": False,
                    "feedback": "Ölümcül hata!"
                },
                {
                    "text": "Yara sadece pudralanmalıdır.",
                    "isCorrect": False,
                    "feedback": "Malpraktis."
                }
            ]
        )
    }

def build_extra_causal_chains():
    """4 ekstra mekanizma zinciri (causal_chain)."""
    return {
        25: make_causal_chain(
            "Alkol Kötüye Kullanımında Karaciğer Steatozu Zinciri",
            [
                "1. Aşırı Etanol Alımı: Alkol dehidrogenaz enzimi sitozolde etanolü asetaldehite yıkar.",
                "2. Yüksek NADH/NAD+ Oranı: Aşırı NADH üretimi mitokondriyal yağ asidi oksidasyonunu durdurur.",
                "3. Trigliserit Sentez Patlaması: Okside edilemeyen yağ asitleri gliserolle birleşerek trigliserite çevrilir.",
                "4. Apoprotein Yetersizliği: Yağlar VLDL paketine konulamaz ve hepatosit sitoplazmasında göllenir.",
                "5. Makroveziküler Steatoz: Tek büyük yağ vakuolü çekirdeği hücre zarına iterek karaciğeri sarartır."
            ]
        ),
        44: make_causal_chain(
            "Böbrek İskemik Koagülatif Enfarktüs Zinciri",
            [
                "1. Arter Tıkanması: Segmental renal arter dalı emboli ile tıkanır.",
                "2. Akut Hipoksi ve Asidoz: Tübül epitelinde ATP biter, laktik asidoz tüm enzimleri kilitler.",
                "3. Protein Koagülasyonu: Hem yapısal proteinler hem de lizozom enzimleri pıhtılaşır.",
                "4. Hayalet Hücreler: Çekirdekler karyolizisle erirken hücre konturları ve glomerül taslağı ayakta kalır.",
                "5. Demarkasyon ve Skar: Çevre canlı dokudan nötrofiller sızar ve aylar sonra kama şeklinde beyaz fibröz skar oluşur."
            ]
        ),
        62: make_causal_chain(
            "Apoptozda Internükleozomal DNA Merdiveni Zinciri",
            [
                "1. Ölüm Sinyali: İntrinsik veya ekstrinsik yolakla efektör kaspaz-3 ve kaspaz-7 aktive olur.",
                "2. ICAD Kesimi: Kaspaz-3, CAD enzimini tutan inhibitör proteini (ICAD) keserek parçalar.",
                "3. Serbest CAD Aktivasyonu: Serbest kalan kaspazla aktive deoksiribonükleaz (CAD) nükleusa girer.",
                "4. Nükleozom Arası Kesim: CAD sadece nükleozomların bağlayıcı DNA kısımlarını 180-200 bp aralıklarla keser.",
                "5. Elektroforetik Merdiven: Jel üzerinde düzenli basamaklar halinde 'DNA ladder' deseni belirir."
            ]
        ),
        86: make_causal_chain(
            "Fournier Gangreninin Fasiyal Yayılım Zinciri",
            [
                "1. Perineal İnokülasyon: Perianal apse veya ürolojik travmayla karma bakteri florası dokuya girer.",
                "2. Sinerjistik Toksin Salınımı: Aerop ve anaerop bakteriler doku fasyalarını eriten enzimler salar.",
                "3. Mikrovasküler Tromboz: Subkutan besleyici damarlar tıkanır ve ciltte masif iskemi gelişir.",
                "4. Fasiyal Tırmanış: Enfeksiyon Colles fasyasından Scarpa fasyasına doğru karın duvarına hızla yayılır.",
                "5. Fulminan Gangren: Cilt dökülür, krepitasyon oluşur ve acil cerrahi debridman yapılmazsa septik şok öldürür."
            ]
        )
    }

def build_extra_interactive_tables(steps_dict):
    """10 adımda coreContent.table'dan zenginleştirilmiş maskeli interaktif tablolar."""
    target_steps = [3, 5, 11, 21, 31, 41, 51, 61, 71, 81]
    extra_tables = {}

    for s_num in target_steps:
        s = steps_dict.get(s_num)
        if not s or not s.get("coreContent", {}).get("table"):
            continue
        tb = s["coreContent"]["table"]
        orig_title = clean_table_title(tb.get("title", f"Adım {s_num} Karşılaştırma Tablosu"))
        headers = tb.get("headers", ["Özellik", "Durum A", "Durum B"])
        rows = tb.get("rows", [])
        if not rows:
            continue

        formatted_rows = []
        for r in rows:
            cells = []
            cells.append({"text": str(r[0]), "isMasked": False, "hint": ""})
            mask_col = 1 if len(r) > 1 else 0
            for col_idx in range(1, len(r)):
                val = str(r[col_idx])
                if col_idx == mask_col:
                    hint = "Kritik Değer" if "Artar" in val or "Azalır" in val else "Hücresel Yanıt"
                    hint = sanitize_hint(hint, val)
                    cells.append({"text": val, "isMasked": True, "hint": hint})
                else:
                    cells.append({"text": val, "isMasked": False, "hint": ""})
            formatted_rows.append({"cells": cells})

        extra_tables[s_num] = {
            "type": "interactive_table",
            "tableTitle": orig_title,
            "tableHeaders": headers,
            "tableRows": formatted_rows
        }

    return extra_tables

def main():
    print("🚀 Kurul 1 - Ders 4 (Hücre Hasarı ve Nekroz - I) Tam Deste Oluşturucu Başlatılıyor...")
    deck_id = "k1p-k1-04-hucre-hasari-ve-nekroz-i"

    os.makedirs(PACKAGES_DIR, exist_ok=True)
    os.makedirs(DECKS_ITEMS_DIR, exist_ok=True)

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

    steps_dict = {s["slideNumber"]: s for s in raw_steps}

    # Örnek soruları yükle ve normalize et
    questions = []
    if os.path.exists(ORNEK_SORULAR_PATH):
        try:
            with open(ORNEK_SORULAR_PATH, "r", encoding="utf-8") as f:
                qdata = json.load(f)
            for k in qdata.get("kazanimlar", []):
                for q in k.get("sorular", []):
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

    # Ekstra elemanları hazırla
    extra_quizzes = build_extra_micro_quizzes()
    extra_branching = build_extra_branching_logic()
    extra_causal = build_extra_causal_chains()
    extra_tables = build_extra_interactive_tables(steps_dict)

    final_slides = []
    for s in raw_steps:
        slide_num = s["slideNumber"]
        is_checkpoint = s.get("isCheckpoint", False)
        checkpoint_num = s.get("checkpointNumber", None)

        # Tablo başlığını temizle
        if s.get("coreContent", {}).get("table"):
            orig_title = s["coreContent"]["table"].get("title", "")
            s["coreContent"]["table"]["title"] = clean_table_title(orig_title)

        current_elems = list(s.get("interactiveElements", []))

        # Ekstra elemanları enjekte et
        if slide_num in extra_quizzes:
            current_elems.append(extra_quizzes[slide_num])
        if slide_num in extra_branching:
            current_elems.append(extra_branching[slide_num])
        if slide_num in extra_causal:
            current_elems.append(extra_causal[slide_num])
        if slide_num in extra_tables:
            current_elems.append(extra_tables[slide_num])

        # Eğer bir adımda birden fazla cloze varsa sadece 1 tanesini bırak (denge için)
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

        # Sızıntı kontrolü ve uyumluluk normalizasyonu
        for el in current_elems:
            t = el.get("type")
            if t == "branching_logic":
                if "options" not in el and "branchingOptions" in el:
                    el["options"] = el["branchingOptions"]
                elif "branchingOptions" not in el and "options" in el:
                    el["branchingOptions"] = el["options"]
            elif t == "cloze_masking":
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

        # İlgili soruları dağıt
        start_q_idx = ((slide_num - 1) * len(questions)) // 100
        end_q_idx = (slide_num * len(questions)) // 100
        step_questions = questions[start_q_idx:end_q_idx]
        if not step_questions and questions:
            step_questions = [questions[(slide_num - 1) % len(questions)]]

        flashcards = s.get("flashcards", [])
        core_content = s.get("coreContent", {})
        if "keyBullets" not in core_content:
            core_content["keyBullets"] = [
                {
                    "title": s["title"],
                    "desc": s["subtitle"],
                    "isKey": True
                }
            ]

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
            "badge": "Tekrar Sayfası" if is_checkpoint else s.get("badge", "Hücre Hasarı"),
            "badgeColor": "teal" if is_checkpoint else s.get("badgeColor", "red"),
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
                "fileName": "2)Hücre Hasarı ve Nekroz.pdf",
                "fileId": "k1-04",
                "startPage": min(65, max(1, (slide_num * 65) // 100)),
                "endPage": min(65, max(1, ((slide_num * 65) // 100) + 1)),
                "primaryPage": min(65, max(1, (slide_num * 65) // 100)),
                "citation": f"Slayt {slide_num} · Kurul 1 Tıbbi Patoloji Sunumu (Prof. Dr. Hikmet Keleş)"
            },
            "aiPromptSuggestions": [
                f"{s['title']} konusunun biyokimyasal ve morfolojik mekanizmasını bir klinik olguyla açıklar mısın?",
                "Bu adımdaki hasar veya nekroz tipinin TUS ve kurul sınavlarındaki ayırıcı tanılarını gösterir misin?"
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

    # 1. MANIFEST.JSON
    manifest_data = {
        "id": "k1-04-hucre-hasari-ve-nekroz-i",
        "title": "Hücre Hasarı ve Nekroz - I (Yeni Mikro-Ders)",
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

    # 2. STRUCTURE.XML
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

        blocks_node = ET.SubElement(slide_node, "layoutBlocks")
        for b in s["layoutBlocks"]:
            ET.SubElement(blocks_node, "block", id=b["id"], type=b["type"], order=str(b["order"]))

        int_node = ET.SubElement(slide_node, "interactiveElements", count=str(len(s["interactiveElements"])))
        for el in s["interactiveElements"]:
            ET.SubElement(int_node, "element", type=el.get("type", ""))

        if s["flashcards"]:
            fc_node = ET.SubElement(slide_node, "flashcards", count=str(len(s["flashcards"])))
            for fc in s["flashcards"]:
                card_node = ET.SubElement(fc_node, "card", id=fc["id"])
                ET.SubElement(card_node, "front").text = fc["front"]
                ET.SubElement(card_node, "back").text = fc["back"]

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

    # 3. BLOCKS.HTML
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

    # 4. CONTENT.MD
    md_lines = [
        "# Hücre Hasarı ve Nekroz - I (Kurul 1 - Ders 4)",
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

    # 5. RUNTIME ITEM JSON
    deck_data = {
        "id": deck_id,
        "title": "Hücre Hasarı ve Nekroz - I (Yeni Mikro-Ders)",
        "shortTitle": "Hücre Hasarı ve Nekroz - I",
        "discipline": "Tıbbi Patoloji",
        "committee": "Kurul 1 (Ürogenital ve Obstetrik)",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "audioFile": "audios/kurul1/k1-04-hucre-hasari-ve-nekroz-i.mp3",
        "audioDuration": "52:10",
        "confidence": "Yüksek",
        "themeColor": "red",
        "matchedNoteId": "k1-04-hucre-hasari-ve-nekroz-i",
        "matchedNoteTitle": "Hücre Hasarı ve Nekroz - I Ders Özeti",
        "isNew": True,
        "isLegacy": False,
        "version": 2,
        "packageSources": {
            "manifest": "packages/k1-04-hucre-hasari-ve-nekroz-i/manifest.json",
            "structureXml": "packages/k1-04-hucre-hasari-ve-nekroz-i/structure.xml",
            "blocksHtml": "packages/k1-04-hucre-hasari-ve-nekroz-i/blocks.html",
            "contentMd": "packages/k1-04-hucre-hasari-ve-nekroz-i/content.md"
        },
        "overview": f"Bu interaktif mikro-öğrenme destesi; 100 atomik adımda, 10 kontrol noktası tekrar sayfasında gömülü akıl kartlarıyla, {total_elems} adet dengeli interaktif alıştırmayla (mikro-quiz, maskeli tablo, dallanan klinik senaryolar, aktif hatırlama, karşılaştırma kaydırıcısı, mekanizma zinciri) hücre hasarının etiyolojisini, geri dönüşümlü hidropik şişmeyi ve steatozu, 'point of no return' mitokondri ve membran kriterlerini, nekrozun sitoplazmik/nükleer morfolojisini (piknoz, karyoreksis, karyolizis), koagülatif enfarktları, serebral ve piyojenik sıvılaşma nekrozunu ve gangren tiplerini derinlemesine öğretir.",
        "highYieldPearls": [
            "📌 [SINAV SPOTU] Hücre hasarının en sık nedeni hipoksi ve iskemidir.",
            "📌 [SINAV SPOTU] En erken geri dönüşümlü morfolojik bulgu hücresel şişmedir (hidropik değişim); ATP azalması sonucu Na+/K+ ATPaz iflasıyla gelişir.",
            "🚨 [KRİTİK UYARI] Geri dönüşümlü hasarda plazma membranı sağlamdır; membran delindiğinde hücre içi enzimler kana sızar ve nekroz başlar.",
            "📌 [SINAV SPOTU] Geri dönüşümsüz hasarın kesin ultrastrüktürel kanıtı: Mitokondri matriksinde elektron-yoğun amorf kalsiyum birikintileri ve membran yırtıklarıdır.",
            "📌 [SINAV SPOTU] Nekrozun sitoplazmik bulguları: Artmış eozinofili (protein denatürasyonu + RNA kaybı), camsı homojenlik (glikojen tükenmesi) ve vakuolizasyondur.",
            "📌 [SINAV SPOTU] Nekrozda nükleer değişiklikler sırasıyla: Piknoz (büzülme) → Karyoreksis (parçalanma) → Karyolizisdir (DNAaz ile erime).",
            "📌 [SINAV SPOTU] En sık görülen nekroz tipi Koagülatif nekrozdur; asidoz enzimleri de denatüre ettiği için doku mimarisi günlerce korunur (hayalet hücreler).",
            "🚨 [KRİTİK UYARI] İskemik enfarktlar kural olarak koagülatif nekrozdur; tek istisna SIVILAŞMA (likefaksiyon) nekrozu görülen BEYİN infarktlarıdır.",
            "📌 [SINAV SPOTU] Gangren klinik bir terimdir; Kuru gangren steril koagülatif nekrozdur, Islak gangren süperenfeksiyonlu sıvılaşma nekrozudur, Gazlı gangren Clostridium alfa-toksinine bağlı gazlı miyonekrozdur.",
            "📌 [SINAV SPOTU] İskemiye tolerans süreleri: Nöron 3-5 dakika, Kalp kası 20-30 dakika, İskelet kası 2-3 saattir."
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
                entry["title"] = "Hücre Hasarı ve Nekroz - I (Yeni Mikro-Ders)"
                entry["overview"] = deck_data["overview"]
                entry["audioDuration"] = "52:10"
                found = True
                break
        if not found:
            catalog.append({
                "id": deck_id,
                "title": "Hücre Hasarı ve Nekroz - I (Yeni Mikro-Ders)",
                "shortTitle": "Hücre Hasarı ve Nekroz - I",
                "discipline": "Tıbbi Patoloji",
                "committee": "Kurul 1 (Ürogenital ve Obstetrik)",
                "instructor": "Prof. Dr. Hikmet Keleş",
                "totalSlides": 100,
                "isNew": True,
                "isLegacy": False,
                "version": 2,
                "audioDuration": "52:10",
                "overview": deck_data["overview"]
            })
        with open(CATALOG_PATH, "w", encoding="utf-8") as f:
            json.dump(catalog, f, ensure_ascii=False, indent=2)
        print(f"7. Catalog JSON güncellendi: {CATALOG_PATH}")

    print("\n✅ TÜM DERS 4 MULTI-FORMAT İŞLEMLERİ BAŞARIYLA TAMAMLANDI!")

if __name__ == "__main__":
    main()
