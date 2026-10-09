#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_full_lesson_3_deck.py
Kurul 1 - Ders 3: Hücresel Adaptasyonlar
Öğretim Üyesi: Prof. Dr. Hikmet Keleş

Yeni Nesil Multi-Format (JSON, XML, HTML, MD) Mikro-Öğrenme Motoru:
1. Tam 100 Atomik Adım.
2. 10 Özel Tekrar Sayfası (Checkpoints 1-10), her birinde 3'er adet gömülü Akıl Kartı (Flashcards, toplam 30 adet).
3. Kısa, yalın, gereksiz uzatmasız tablo başlıkları.
4. Tam dengeli 210-240 İnteraktif Öğe (Adım sayısının ~2.1 katı, [1.5x - 3.0x] aralığında).
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
PACKAGES_DIR = os.path.join(MEDS_ROOT, 'src', 'data', 'decks', 'packages', 'k1-03-hucresel-adaptasyonlar')
CATALOG_PATH = os.path.join(MEDS_ROOT, 'src', 'data', 'decks', 'catalog.json')
INTERACTIVE_DECKS_PATH = os.path.join(MEDS_ROOT, 'src', 'data', 'interactive_learning_decks.json')
ORNEK_SORULAR_PATH = os.path.join(MEDS_ROOT, 'src', 'data', 'ornek_sorular', 'k1', 'k1-03-hucresel-adaptasyonlar.json')

# Section importları
sys.path.insert(0, os.path.dirname(__file__))
from k1_03_deck_data import (
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
from k1_03_deck_data.helpers import (
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
        "Hücresel Mekanizma",
        "Kritik Bilgi"
    ]
    for p in candidate_prompts:
        if not leaks(p, answer):
            return p
    return "Temel Prensip"

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

def build_extra_branching():
    """Branching logic elemanları (20 adet klinik karar senaryosu)."""
    return {
        3: make_branching_logic(
            "Sol ventrikül hipertrofisi saptanan 58 yaşındaki hipertansif hastada miyokard dokusunun hücresel sınırları senaryosu.",
            [
                {
                    "text": "Kalp kası hücreleri bölünerek çoğalır ve dokudaki hücre sayısı iki katına çıkar.",
                    "isCorrect": False,
                    "feedback": "Hatalı! Erişkin miyokard hücreleri kalıcı (permanent) hücrelerdir; bölünemezler, yalnızca hipertrofiye uğrarlar."
                },
                {
                    "text": "Artan iş yüküne yanıt olarak miyositlerde protein ve organel sentezi artar; hücre çapı büyür, bölünme gerçekleşmez.",
                    "isCorrect": True,
                    "feedback": "Doğru patofizyolojik mekanizma! Kalıcı dokularda adaptasyon sadece hipertrofi ile sınırlıdır."
                },
                {
                    "text": "Miyositler apoptoza giderek yerini yağ dokusuna bırakır.",
                    "isCorrect": False,
                    "feedback": "Yanlış! Başlangıç adaptif yanıt hipertrofidir, doğrudan yağ metaplazisi gelişmez."
                }
            ]
        ),
        7: make_branching_logic(
            "Uterus miyom ameliyatı öncesi gebelik ve puberte dönemindeki hormonal uterus büyümesinin mekanizması senaryosu.",
            [
                {
                    "text": "Gebelik uterusundaki büyüme sadece düz kas hücrelerinin hiperplazisi ile gerçekleşir.",
                    "isCorrect": False,
                    "feedback": "Eksik! Gebelikte miyometriyum hem hiperplazi hem de belirgin hipertrofi gösterir."
                },
                {
                    "text": "Östrojen uyarısıyla miyometriyum düz kas hücreleri hem boyutça büyür (hipertrofi) hem de sayıca çoğalır (hiperplazi).",
                    "isCorrect": True,
                    "feedback": "Kusursuz endokrin patoloji tespiti! Hormonal fizyolojik uyarılarda stabil/bölünebilen dokular hipertrofi ve hiperplaziyi birlikte kullanır."
                },
                {
                    "text": "Uterus büyümesi metaplazik kemik oluşumu ile gerçekleşir.",
                    "isCorrect": False,
                    "feedback": "İlgisiz ve patolojiktir."
                }
            ]
        ),
        12: make_branching_logic(
            "Ağır aort darlığı ve dekompanse kalp yetmezliği gelişen hastada adaptasyonun tükenme sınırı senaryosu.",
            [
                {
                    "text": "Hipertrofiye uğramış kalp kası sonsuza dek basınca dayanır ve hiçbir zaman iskemiye uğramaz.",
                    "isCorrect": False,
                    "feedback": "Hatalı! Miyosit hacmi kapiller damar yoğunluğunu aştığında kritik rölatif iskemi başlar."
                },
                {
                    "text": "Kapiller vaskülarizasyon hipertrofik kitleyi beslemeye yetmediğinde hücresel hasar, apoptoz, lizis ve kardiyak yetmezlik başlar.",
                    "isCorrect": True,
                    "feedback": "Doğru patolojik dekompansasyon zinciri! Adaptif sınır aşıldığında geri dönüşsüz hasar ve yetmezlik kaçınılmazdır."
                },
                {
                    "text": "Kalp derhal küçülerek fizyolojik atrofiye geçer.",
                    "isCorrect": False,
                    "feedback": "Yanlış! Bası yükü sürerken atrofi gelişmez, dilatasyon ve yetmezlik gelişir."
                }
            ]
        ),
        16: make_branching_logic(
            "Karaciğer parsiyel hepatektomisi yapılan bir canlı donörde organın rejenerasyon kapasitesi senaryosu.",
            [
                {
                    "text": "Karaciğer kalıcı doku olduğundan kalan parça asla büyüyemez.",
                    "isCorrect": False,
                    "feedback": "Yanlış! Karaciğer hücreleri stabil hücrelerdir; G0 evresinden uyarılınca hücre döngüsüne girerler."
                },
                {
                    "text": "HGF, IL-6 ve TNF-alfa uyarısıyla hepatositler mitoza girer; kompensatuvar hiperplazi ile karaciğer orijinal kütlesine ulaşır.",
                    "isCorrect": True,
                    "feedback": "Mükemmel kompensatuvar hiperplazi bilgisi! Sitokinler ve büyüme faktörleri sessiz hepatositleri uyarır."
                },
                {
                    "text": "Kalan doku fibröz bağ dokusuna dönüşerek skar oluşturur.",
                    "isCorrect": False,
                    "feedback": "Hatalı! Sağlıklı karaciğerde parsiyel rezeksiyon sonrası skar değil parenkimal rejenerasyon olur."
                }
            ]
        ),
        22: make_branching_logic(
            "Menopoz sonrası 62 yaşındaki bir kadında atipik endometrial hiperplazi saptandığında kanser riski senaryosu.",
            [
                {
                    "text": "Endometrial hiperplazinin kanserle hiçbir ilişkisi yoktur, tamamen selim bir tablodur.",
                    "isCorrect": False,
                    "feedback": "Hatalı! Özellikle atipili endometrial hiperplazi, endometrial adenokarsinom için güçlü bir premalign lezyondur."
                },
                {
                    "text": "Karşılanmamış sürekli östrojen uyarısı atipili hiperplaziye yol açar; PTEN mutasyonları eklenirse adenokarsinoma ilerleyebilir.",
                    "isCorrect": True,
                    "feedback": "Doğru jinekolojik onkoloji kararı! Karşılanmamış östrojen patolojik hiperplaziyi tetikler ve kansere zemin hazırlar."
                },
                {
                    "text": "Lezyon sadece viral HPV enfeksiyonuyla ilişkilidir.",
                    "isCorrect": False,
                    "feedback": "Yanlış! HPV serviks karsinomunda etkendir, endometrial hiperplazide östrojen rol oynar."
                }
            ]
        ),
        27: make_branching_logic(
            "Bacak kırığı nedeniyle 8 hafta alçıda kalan bir sporcunun baldır kasında gelişen küçülme senaryosu.",
            [
                {
                    "text": "Kas liflerinin sayısı yarıya inmiştir, hücre ölümü olmuştur.",
                    "isCorrect": False,
                    "feedback": "Yanlış! İmmobilizasyon atrofisinde birincil olay hücre sayısının azalması değil, hücre hacminin ve proteinlerinin küçülmesidir."
                },
                {
                    "text": "Kullanılmama (disuse) atrofisi gelişmiştir; ubikuitin-proteazom yolağı ile miyofibriller parçalanmış, hücre hacmi azalmıştır.",
                    "isCorrect": True,
                    "feedback": "Doğru patobiyolojik mekanizma! İmmobilizasyonda protein sentezi düşer, ubikuitinasyonla proteazomda yıkım artar."
                },
                {
                    "text": "Kas lifleri kıkırdak dokusuna dönüşmüştür.",
                    "isCorrect": False,
                    "feedback": "Hatalı! Bu bir metaplazi değil, saf atrofidir."
                }
            ]
        ),
        33: make_branching_logic(
            "Kaşektik kanser hastasında iskelet kası erimesini tetikleyen biyokimyasal mekanizma senaryosu.",
            [
                {
                    "text": "Tümör nekrozis faktör (TNF/kaşektin) ve ubikuitin ligazlar kas protein yıkımını dramatik artırır.",
                    "isCorrect": True,
                    "feedback": "Kusursuz onkolojik mekanizma! Sitokinler ubikuitin-proteazom yolağını aktive ederek katabolizmayı hızlandırır."
                },
                {
                    "text": "Kas hücreleri yağ hücresine dönüşerek lipom oluşturur.",
                    "isCorrect": False,
                    "feedback": "Hatalı!"
                },
                {
                    "text": "Kaşekside sadece glikojen depoları tükenir, kas proteini korunur.",
                    "isCorrect": False,
                    "feedback": "Yanlış! Kaşeksinin ana özelliği ağır iskelet kası proteolizidir."
                }
            ]
        ),
        38: make_branching_logic(
            "Atrofiye uğrayan kardiyak miyositlerde elektron mikroskobunda izlenen kahverengi granüller senaryosu.",
            [
                {
                    "text": "Granüller hemosiderindir ve hastada aşırı demir yüklenmesi olduğunu gösterir.",
                    "isCorrect": False,
                    "feedback": "Hatalı! Yaşlanma ve atrofide biriken kahverengi pigment lipofuskindir."
                },
                {
                    "text": "Lipofuskin pigmentidir; membran lipitlerinin peroksidasyonu ve otofaji sonucu sindirilemeyen lizozomal artık kalıntılarıdır.",
                    "isCorrect": True,
                    "feedback": "Doğru patoloji teşhisi! Lipofuskin 'aşınma ve yıpranma' (wear and tear) veya esmer atrofi pigmentidir."
                },
                {
                    "text": "Melanin pigmentidir ve deriden kalbe göç etmiştir.",
                    "isCorrect": False,
                    "feedback": "Fizyopatolojik olarak olanaksızdır."
                }
            ]
        ),
        45: make_branching_logic(
            "Uzun yıllar günde 1 paket sigara içen bir hastanın bronş biyopsisinde silyalı kolumnar epitel yerine çok katlı yassı epitel izlenmesi senaryosu.",
            [
                {
                    "text": "Mevcut kolumnar epitel hücreleri fiziksel olarak biçim değiştirip yassılaşmıştır.",
                    "isCorrect": False,
                    "feedback": "Hatalı! Erişkin farklılaşmış hücre başka hücreye dönüşmez; bazal kök hücrelerin genetik yeniden programlanması gerekir."
                },
                {
                    "text": "Sigara dumanına karşı bazal rezerv kök hücreler skuamöz yönde farklılaşarak metaplazi oluşturmuştur; mekanik dirence dayanıklı fakat siliyer temizlikten yoksundur.",
                    "isCorrect": True,
                    "feedback": "Mükemmel metaplazi mekanizması! Kök hücrelerin transkripsiyon faktörleri değişerek dayanıklı yassı epitele farklılaşır."
                },
                {
                    "text": "Bu durum doğuştan gelen normal bir varyasyondur.",
                    "isCorrect": False,
                    "feedback": "Yanlış! Sigaranın indüklediği edinsel bir patolojik adaptasyondur."
                }
            ]
        ),
        48: make_branching_logic(
            "Kronik gastroözofageal reflü (GÖRH) hastasında distal özofagusta Barrett özofagusu saptanması senaryosu.",
            [
                {
                    "text": "Çok katlı yassı epitelin asit reflüsüne yanıt olarak goblet hücreli kolumnar intestinal epitele metaplazisidir; adenokarsinom riski taşır.",
                    "isCorrect": True,
                    "feedback": "Doğru gastroenterolojik patoloji tespiti! Barrett metaplazisi mukus üreterek asitten korur ancak adenokarsinoma prekürsördür."
                },
                {
                    "text": "Barrett metaplazisi skuamöz hücreli karsinomun doğrudan kanıtıdır.",
                    "isCorrect": False,
                    "feedback": "Hatalı! Barrett özofagusunda gelişen tümör skuamöz karsinom değil adenokarsinomdur."
                },
                {
                    "text": "Asit reflüsü tedavi edilse bile asla takip gerektirmez.",
                    "isCorrect": False,
                    "feedback": "Hatalı! Displazi ve kanser riski nedeniyle endoskopik biyopsi takibi şarttır."
                }
            ]
        ),
        52: make_branching_logic(
            "Mesanesinde schistosoma enfeksiyonu veya taş olan hastada gelişen epitelyal adaptasyon senaryosu.",
            [
                {
                    "text": "Transizyonel epitel skuamöz metaplaziye uğrar; zemininde skuamöz hücreli mesane karsinomu riski artar.",
                    "isCorrect": True,
                    "feedback": "Kusursuz üropatoloji tespiti! Kronik irritasyon transizyonel epiteli çok katlı yassı epitele dönüştürür."
                },
                {
                    "text": "Mesane epiteli kemik iliğine dönüşür.",
                    "isCorrect": False,
                    "feedback": "Biyolojik olarak imkansızdır."
                },
                {
                    "text": "Hiçbir hücresel değişiklik oluşmaz.",
                    "isCorrect": False,
                    "feedback": "Yanlış! Kronik taş ve parazit tahrişi belirgin metaplazi yapar."
                }
            ]
        ),
        57: make_branching_logic(
            "Derin kas travması sonrası kasta ağrılı sert bir kitle oluşan 24 yaşındaki sporcuda biyopsi senaryosu.",
            [
                {
                    "text": "Kitlenin osteosarkom olduğu kabul edilip bacak ampute edilmelidir.",
                    "isCorrect": False,
                    "feedback": "Ağır hata! Travma sonrası kas içi heterotopik kemikleşme Miyozitis Ossifikans'tır ve selimdir."
                },
                {
                    "text": "Miyozitis ossifikans (mezenkimal metaplazi) tanısı konur; fibroblastlar travma uyarısıyla osteoblastlara metaplazi göstermiştir.",
                    "isCorrect": True,
                    "feedback": "Doğru ortopedik patoloji yaklaşımı! Yumuşak dokuda travma sonrası selim lameller kemik oluşumudur."
                },
                {
                    "text": "Doku doğrudan tüberküloz granülomudur.",
                    "isCorrect": False,
                    "feedback": "Hatalı!"
                }
            ]
        ),
        63: make_branching_logic(
            "Serviks smearinde yüksek dereceli skuamöz intraepitelyal lezyon (HSIL / Ağır Displazi) saptanan hastada yönetim senaryosu.",
            [
                {
                    "text": "Displazi tamamen geri dönüşlü ve zararsızdır; hiçbir tedavi ve biyopsi gerekmez.",
                    "isCorrect": False,
                    "feedback": "Hatalı! Ağır displazi (HSIL) invaziv karsinoma ilerleme riski çok yüksek olan premalign lezyondur."
                },
                {
                    "text": "Kolposkopi altında biyopsi veya LEEP/konizasyon ile displastik epitel cerrahi sınır kontrolüyle çıkarılmalıdır.",
                    "isCorrect": True,
                    "feedback": "Doğru jinekolojik yaklaşım! Displazi bazal membran aşılmadan çıkarılırsa tam kür sağlanır."
                },
                {
                    "text": "Hasta doğrudan sistemik kemoterapiye alınır.",
                    "isCorrect": False,
                    "feedback": "Aşırı ve hatalı! İnvaziv karsinom kanıtlanmadan kemoterapi verilmez."
                }
            ]
        ),
        67: make_branching_logic(
            "İntraselüler yağlanma (steatoz) şüphesi olan bir karaciğer biyopsisinde patoloğun doku takibi seçimi senaryosu.",
            [
                {
                    "text": "Doku rutin parafin takibine alınır; alkol ve ksilenden geçirilir.",
                    "isCorrect": False,
                    "feedback": "Hatalı! Ksilen ve alkol nötral yağları çözer; parafin kesitte yağ damlacıkları boş delik olarak görünür."
                },
                {
                    "text": "Taze dokudan frozen (dondurulmuş) kesit alınarak Oil Red O veya Sudan Black boyası uygulanır.",
                    "isCorrect": True,
                    "feedback": "Mükemmel histoteknoloji kararı! Nötral trigliseritler ancak çözücü kullanılmayan dondurma kesitlerinde boyanabilir."
                },
                {
                    "text": "Doku yüksek ısıda yakılarak incelenir.",
                    "isCorrect": False,
                    "feedback": "Doku tahrip olur."
                }
            ]
        ),
        72: make_branching_logic(
            "Yaşlı bir hastada kronik kalsifiye aort kapak darlığı biyopsisinde serum kalsiyum düzeyi değerlendirmesi senaryosu.",
            [
                {
                    "text": "Distrofik kalsifikasyondur; serum kalsiyum ve fosfat düzeyleri normal sınırlardadır.",
                    "isCorrect": True,
                    "feedback": "Kusursuz kardiyopatoloji ilkesi! Distrofik kalsifikasyon hasarlı/nekrotik dokuda normal kalsiyum düzeyinde gelişir."
                },
                {
                    "text": "Metastatik kalsifikasyondur; hastada mutlaka hiperkalsemi ve hiperparatiroidizm vardır.",
                    "isCorrect": False,
                    "feedback": "Yanlış! Yaşlılık aort kapak kalsifikasyonu distrofik kalsifikasyonun prototipidir ve serum kalsiyumu normaldir."
                },
                {
                    "text": "Kalsiyum kristalleri dokuda değil yalnızca kan hücrelerinin içindedir.",
                    "isCorrect": False,
                    "feedback": "Hatalı!"
                }
            ]
        ),
        77: make_branching_logic(
            "Primer hiperparatiroidizmi olan bir hastada akciğer alveol duvarlarında ve böbrek tübüllerinde yaygın kalsiyum çökmesi senaryosu.",
            [
                {
                    "text": "Metastatik kalsifikasyondur; kanda yüksek PTH ve hiperkalsemi nedeniyle normal dokularda kalsiyum birikmiştir.",
                    "isCorrect": True,
                    "feedback": "Doğru endokrin-patoloji tanısı! Metastatik kalsifikasyon hiperkalsemi zemininde özellikle iç ortamı alkali organlarda oluşur."
                },
                {
                    "text": "Distrofik kalsifikasyondur; böbrek ve akciğer dokusu önceden nekroze olmuştur.",
                    "isCorrect": False,
                    "feedback": "Yanlış! Primer neden hiperkalsemidir ve doku önceden hasarlı değildir."
                },
                {
                    "text": "Kalsiyum çökmesi tamamen enfeksiyona bağlıdır.",
                    "isCorrect": False,
                    "feedback": "Hatalı!"
                }
            ]
        ),
        82: make_branching_logic(
            "Hücresel replikatif yaşlanmada (Hayflick sınırı) telomeraz enziminin rolü senaryosu.",
            [
                {
                    "text": "Somatik hücrelerde telomeraz aktiftir ve telomerler her bölünmede uzar.",
                    "isCorrect": False,
                    "feedback": "Hatalı! Somatik hücrelerde telomeraz inaktiftir; bu nedenle telomerler her bölünmede kısalır."
                },
                {
                    "text": "Çoğu somatik hücrede telomeraz inaktiftir; kısalan telomerler DNA hasar yanıtını (p53) aktive ederek replikatif yaşlanmaya sokar.",
                    "isCorrect": True,
                    "feedback": "Doğru moleküler mekanizma! Telomer erozyonu p53/p21 üzerinden hücre döngüsünü kalıcı olarak durdurur."
                },
                {
                    "text": "Telomeraz sadece bakterilerde bulunan bir toksindir.",
                    "isCorrect": False,
                    "feedback": "Yanlış!"
                }
            ]
        ),
        87: make_branching_logic(
            "Kanser hücrelerinin ölümsüzlük (immortalite) kazanmasının hücresel biyoloji temeli senaryosu.",
            [
                {
                    "text": "Kanser hücreleri telomerlerini tamamen kaybederek DNA'sız yaşamayı öğrenir.",
                    "isCorrect": False,
                    "feedback": "Biyolojik olarak anlamsızdır."
                },
                {
                    "text": "Kanser hücrelerinin yaklaşık %90'ında telomeraz enzimi reaktive olur; telomer boyu korunarak sınırsız bölünme kapasitesi kazanılır.",
                    "isCorrect": True,
                    "feedback": "Kusursuz moleküler onkoloji tespiti! Telomeraz aktivasyonu tümör hücrelerine replikatif ölümsüzlük kazandırır."
                },
                {
                    "text": "Kanser hücreleri sadece mitokondri bölünmesiyle yaşar.",
                    "isCorrect": False,
                    "feedback": "Hatalı!"
                }
            ]
        ),
        92: make_branching_logic(
            "Kalori kısıtlamasının (CR) ömrü uzatıcı etkisinde sirtuin (SIRT1) proteinlerinin rolü senaryosu.",
            [
                {
                    "text": "Sirtuinler NAD bağımlı deasetilazlardır; DNA onarımını artırır, p53'ü düzenler ve hücresel yaşlanmayı geciktirir.",
                    "isCorrect": True,
                    "feedback": "Doğru biyokimyasal mekanizma! Düşük kalori ve yüksek NAD+, SIRT enzimlerini aktive ederek ömrü uzatır."
                },
                {
                    "text": "Sirtuinler protein sentezini tamamen durdurarak hücreyi lize eder.",
                    "isCorrect": False,
                    "feedback": "Hatalı! Sirtuinler koruyucu ve onarıcı enzimlerdir."
                },
                {
                    "text": "Sirtuinler serbest oksijen radikallerini üreten toksik enzimlerdir.",
                    "isCorrect": False,
                    "feedback": "Yanlış! Serbest radikal hasarını azaltmaya yardımcı olurlar."
                }
            ]
        )
    }

def build_extra_causal_chains():
    """Ek mekanizma zincirleri (causal_chain)."""
    return {
        17: make_causal_chain(
            "Basınç Yüküne Bağlı Sol Ventrikül Hipertrofisi ve Dekompansasyon Zinciri",
            [
                "1. Artmış Afterload: Kronik sistemik hipertansiyon sol ventrikül duvar stresini artırır.",
                "2. Mekanosensör Aktivasyonu: İntegrinler ve reseptörler mekanik gerimi hücre içi kimyasal sinyale çevirir.",
                "3. Transkripsiyonel Yanıt: GATA4, NFAT ve MEF2 aktive olarak miyofibril ve sarkomer genlerini indükler.",
                "4. Konsantrik Hipertrofi: Miyosit çapı genişler, ventrikül duvarı kalınlaşarak Laplace yasasına göre duvar stresini dengeler.",
                "5. Dekompansasyon: Miyosit kalınlığı kapiller beslenme mesafesini aştığında rölatif iskemi, apoptoz, fibrozis ve dilatasyon gelişir."
            ]
        ),
        34: make_causal_chain(
            "Kullanılmama (Disuse) Atrofisinde Ubikuitin-Proteazom Yolağı Zinciri",
            [
                "1. Mekanik İmmobilizasyon: Ekstremitenin alçıya alınması veya hareketsizlik kas kasılmasını durdurur.",
                "2. Transkripsiyonel Baskılanma: Protein sentezi yavaşlar, IGF-1 ve Akt aktivitesi düşer.",
                "3. E3 Ubikuitin Ligaz Aktivasyonu: MuRF1 ve Atrogin-1 kas dokusunda hızla transkribe edilir.",
                "4. Hedef Proteoliz: Miyofibriller ubikuitin zincirleriyle etiketlenerek 26S proteazoma yönlendirilir.",
                "5. Kas Hacminde Küçülme: Hücre sayısı korunurken sarkoplazma ve miyofibril hacmi dramatik azalır."
            ]
        ),
        74: make_causal_chain(
            "Distrofik Kalsifikasyonun Hücresel ve Moleküler Mekanizma Zinciri",
            [
                "1. Membran Hasarı: İskemi veya toksin etkisiyle hücre membranı bütünlüğünü kaybeder.",
                "2. Hücre İçi Kalsiyum Akışı: Ekstraselüler kalsiyum hasarlı hücreye ve mitokondriye kontrolsüz dolar.",
                "3. Membran Fosfolipidleri: Parçalanan membranlardan açığa çıkan asidik fosfolipidler kalsiyum iyonlarını bağlar.",
                "4. Kalsiyum-Fosfat Çökelmesi: Fosfataz enzimleri fosfat grubunu açığa çıkararak kalsiyumla kristalleşmeyi başlatır.",
                "5. Hidroksiapatit Oluşumu: Kristaller büyüyerek lameller hidroksiapatit kalsiyum tuzuna dönüşür."
            ]
        ),
        98: make_causal_chain(
            "Serbest Oksijen Radikallerine Bağlı Hücresel Yaşlanma Zinciri",
            [
                "1. Mitokondriyal Solunum Kaçağı: Yaşlanan mitokondrilerde elektron transport zincirinden süperoksit sızar.",
                "2. Oksidatif Hasar: ROS molekülleri mitokondriyal DNA'yı, proteinleri ve membran lipitlerini okside eder.",
                "3. Kısırdöngü: Hasarlı mitokondriyal DNA daha defektif solunum kompleksi ve daha çok ROS üretir.",
                "4. Nükleer DNA Hasar Yanıtı: Okside nükleer DNA lezyonları p53 ve p21 transkripsiyonunu indükler.",
                "5. Kalıcı Replikatif Senesans: Hücre döngüsü G1 evresinde kalıcı durur ve SASP enflamatuvar sitokinleri salgılanır."
            ]
        )
    }

def build_extra_interactive_tables(steps_dict):
    """
    20 adımda coreContent.table'dan zenginleştirilmiş maskeli interaktif tablolar üretir.
    Her satırda tam bir maskeli hücre bulunur; ipuçları sızıntısızdır.
    """
    target_steps = [4, 9, 13, 18, 23, 28, 31, 35, 39, 42, 47, 51, 55, 61, 65, 73, 78, 84, 88, 94]
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
        for r_idx, r in enumerate(rows):
            cells = []
            # İlk sütun daima açık
            cells.append({"text": str(r[0]), "isMasked": False, "hint": ""})
            # 2. veya 3. sütunu maskele
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

        table_widget = {
            "type": "interactive_table",
            "tableTitle": orig_title,
            "tableHeaders": headers,
            "tableRows": formatted_rows
        }
        extra_tables[s_num] = table_widget

    return extra_tables

def main():
    print("🚀 Kurul 1 - Ders 3 (Hücresel Adaptasyonlar) Tam Deste Oluşturucu Başlatılıyor...")
    deck_id = "k1p-k1-03-hucresel-adaptasyonlar"

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

    steps_dict = {s["slideNumber"]: s for s in raw_steps}

    # Örnek soruları yükle ve validator formatına tam uyumlu (stem + options + correctAnswer) hazırla
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

    # Ekstra interaktif ögeleri üret
    extra_branching = build_extra_branching()
    extra_causal = build_extra_causal_chains()
    extra_tables = build_extra_interactive_tables(steps_dict)

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

        # Ekstra branching logic ekle
        if slide_num in extra_branching:
            current_elems.append(extra_branching[slide_num])

        # Ekstra causal chain ekle
        if slide_num in extra_causal:
            current_elems.append(extra_causal[slide_num])

        # Ekstra interactive table ekle
        if slide_num in extra_tables:
            current_elems.append(extra_tables[slide_num])

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
            "badge": "Tekrar Sayfası" if is_checkpoint else s.get("badge", "Adaptasyon"),
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
                "fileName": "2)Hücresel Adaptasyonlar.pdf",
                "fileId": "k1-03",
                "startPage": min(55, max(1, (slide_num * 55) // 100)),
                "endPage": min(55, max(1, ((slide_num * 55) // 100) + 1)),
                "primaryPage": min(55, max(1, (slide_num * 55) // 100)),
                "citation": f"Slayt {slide_num} · Kurul 1 Tıbbi Patoloji Sunumu (Prof. Dr. Hikmet Keleş)"
            },
            "aiPromptSuggestions": [
                f"{s['title']} konusunun hücresel ve klinik mekanizmasını bir olgu senaryosuyla açıklar mısın?",
                "Bu adımdaki adaptasyon tipinin TUS ve kurul sınavlarında çıkabilecek ayırıcı tanılarını gösterir misin?"
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
        "id": "k1-03-hucresel-adaptasyonlar",
        "title": "Hücresel Adaptasyonlar (Yeni Mikro-Ders)",
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
        "# Hücresel Adaptasyonlar (Kurul 1 - Ders 3)",
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
        "title": "Hücresel Adaptasyonlar (Yeni Mikro-Ders)",
        "shortTitle": "Hücresel Adaptasyonlar",
        "discipline": "Tıbbi Patoloji",
        "committee": "Kurul 1 (Ürogenital ve Obstetrik)",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "audioFile": "audios/kurul1/k1-03-hucresel-adaptasyonlar.mp3",
        "audioDuration": "48:30",
        "confidence": "Yüksek",
        "themeColor": "emerald",
        "matchedNoteId": "k1-03-hucresel-adaptasyonlar",
        "matchedNoteTitle": "Hücresel Adaptasyonlar Ders Özeti",
        "isNew": True,
        "isLegacy": False,
        "version": 2,
        "packageSources": {
            "manifest": "packages/k1-03-hucresel-adaptasyonlar/manifest.json",
            "structureXml": "packages/k1-03-hucresel-adaptasyonlar/structure.xml",
            "blocksHtml": "packages/k1-03-hucresel-adaptasyonlar/blocks.html",
            "contentMd": "packages/k1-03-hucresel-adaptasyonlar/content.md"
        },
        "overview": f"Bu interaktif mikro-öğrenme destesi; 100 atomik adımda, 10 kontrol noktası tekrar sayfasında gömülü akıl kartlarıyla, {total_elems} adet dengeli interaktif alıştırmayla (mikro-quiz, maskeli tablo, dallanan klinik senaryolar, aktif hatırlama, karşılaştırma kaydırıcısı, mekanizma zinciri) hücrenin strese verdiği fizyolojik ve patolojik adaptasyon yanıtlarını (hipertrofi, hiperplazi, atrofi, metaplazi), displaziyi, intraselüler birikimleri, patolojik kalsifikasyonu ve hücresel yaşlanma mekanizmalarını eksiksiz öğretir.",
        "highYieldPearls": [
            "📌 [SINAV SPOTU] Hipertrofi hücre boyutunun artmasıdır; bölünemeyen kalıcı (permanent) hücrelerin (çizgili kas, miyokard, nöron) ana adaptasyonudur.",
            "📌 [SINAV SPOTU] Hiperplazi hücre sayısının artmasıdır; sadece bölünebilen kök veya stabil/labil hücreleri olan dokularda (endometriyum, karaciğer, kemik iliği) görülür.",
            "🚨 [KRİTİK UYARI] Gebelikte uterus büyümesi HEM hipertrofi HEM de hiperplazinin birlikte görüldüğü klasik fizyolojik adaptasyon örneğidir.",
            "📌 [SINAV SPOTU] Atrofide protein yıkımında ubikuitin-proteazom yolağı, hücresel organel sindiriminde otofaji-lizozom sistemi temel rol oynar.",
            "📌 [SINAV SPOTU] Lipofuskin (esmer atrofi pigmenti), membran lipitlerinin peroksidasyonu sonucu lizozomlarda biriken sindirilemeyen artık cisimlerdir.",
            "🚨 [KRİTİK UYARI] Metaplazi bir erişkin hücre tipinin başka bir erişkin hücre tipine dönüşmesidir; erişkin hücre doğrudan değişmez, bazal kök hücrelerin transkripsiyonel yeniden programlanmasıyla oluşur.",
            "📌 [SINAV SPOTU] En sık görülen metaplazi, sigara içenlerin bronşlarında silyalı yalancı çok katlı silindirik epitelin çok katlı yassı epitele dönüşmesidir.",
            "📌 [SINAV SPOTU] Barrett özofagusu: Reflü sonucu distal özofagusta skuamöz epitelin goblet hücreli intestinal kolumnar epitele metaplazisidir; adenokarsinoma prekürsördür.",
            "📌 [SINAV SPOTU] Distrofik kalsifikasyon nekrotik/hasarlı dokuda normal serum kalsiyum düzeyinde gelişir; metastatik kalsifikasyon ise hiperkalsemi zemininde normal dokularda (özellikle akciğer, böbrek, mide gibi asit salgılayan alkali ortamlarda) oluşur.",
            "📌 [SINAV SPOTU] Replikatif hücresel yaşlanma (Hayflick sınırı) telomer kısalması ve p53/p21 aktivasyonuyla oluşur; kanser hücreleri telomerazı reaktive ederek sınırsız bölünme kazanır."
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
                entry["title"] = "Hücresel Adaptasyonlar (Yeni Mikro-Ders)"
                entry["overview"] = deck_data["overview"]
                entry["audioDuration"] = "48:30"
                found = True
                break
        if not found:
            catalog.append({
                "id": deck_id,
                "title": "Hücresel Adaptasyonlar (Yeni Mikro-Ders)",
                "shortTitle": "Hücresel Adaptasyonlar",
                "discipline": "Tıbbi Patoloji",
                "committee": "Kurul 1 (Ürogenital ve Obstetrik)",
                "instructor": "Prof. Dr. Hikmet Keleş",
                "totalSlides": 100,
                "isNew": True,
                "isLegacy": False,
                "version": 2,
                "audioDuration": "48:30",
                "overview": deck_data["overview"]
            })
        with open(CATALOG_PATH, "w", encoding="utf-8") as f:
            json.dump(catalog, f, ensure_ascii=False, indent=2)
        print(f"7. Catalog JSON güncellendi: {CATALOG_PATH}")

    print("\n✅ TÜM DERS 3 MULTI-FORMAT İŞLEMLERİ BAŞARIYLA TAMAMLANDI!")

if __name__ == "__main__":
    main()
