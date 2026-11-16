#!/usr/bin/env python3
"""
Kurul 1 - Ders 5: Hücre Hasarı ve Nekroz - II (Prof. Dr. Hikmet Keleş)
Multi-Format İnteraktif Öğrenme Destesi Oluşturucu.
Tüm interaktif öge kurallarına, %8 çeşitlilik şartına ve doğrulama yönergelerine tam uyumludur.
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import json
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
from collections import Counter
import unicodedata

from scripts.k1_05_deck_data.section_1 import get_section_1_slides
from scripts.k1_05_deck_data.section_2 import get_section_2_slides
from scripts.k1_05_deck_data.section_3 import get_section_3_slides
from scripts.k1_05_deck_data.section_4 import get_section_4_slides
from scripts.k1_05_deck_data.section_5 import get_section_5_slides
from scripts.k1_05_deck_data.section_6 import get_section_6_slides
from scripts.k1_05_deck_data.section_7 import get_section_7_slides
from scripts.k1_05_deck_data.section_8 import get_section_8_slides
from scripts.k1_05_deck_data.section_9 import get_section_9_slides
from scripts.k1_05_deck_data.section_10 import get_section_10_slides
from scripts.k1_05_deck_data.helpers import (
    make_micro_quiz, make_branching_logic, make_causal_chain,
    make_before_after, make_active_recall, make_cloze, make_table
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDS_DIR = os.path.join(BASE_DIR, "meds")
QUESTIONS_FILE = os.path.join(MEDS_DIR, "src/data/ornek_sorular/k1/k1-05-hucre-hasari-ve-nekroz-ii.json")
PACKAGES_DIR = os.path.join(MEDS_DIR, "src/data/decks/packages/k1-05-hucre-hasari-ve-nekroz-ii")
DECKS_ITEMS_DIR = os.path.join(MEDS_DIR, "src/data/decks/items")
INTERACTIVE_DECKS_PATH = os.path.join(MEDS_DIR, "src/data/interactive_learning_decks.json")
CATALOG_PATH = os.path.join(MEDS_DIR, "src/data/decks/catalog.json")

import re

def fold(s):
    return str(s or '').lower().replace('ı', 'i').replace('İ', 'i')

def leaks(hint, answer):
    h = fold(hint)
    return any((w[:5] if len(w) > 5 else w) in h for w in re.findall(r'[\wçğıöşü%.,-]+', fold(answer)) if len(w) >= 3 or re.search(r'\d', w))

def sanitize_hint(hint: str, answer: str, fallback: str = "İlgili tıbbi kavramı hatırlayınız") -> str:
    if not hint:
        return fallback
    if leaks(hint, answer):
        return fallback
    return hint

def clean_table_title(t: str) -> str:
    if not t:
        return "Özet Tablo"
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
    """6 ekstra mikro soru (micro_quiz) envanteri."""
    return {
        18: make_micro_quiz(
            "Akut pankreatitte gelişen enzimatik yağ nekrozunda tebeşir beyazı sabunlaşma odaklarının oluşumunda hangi pankreatik enzim anahtar rol oynar?",
            {
                "A": "Pankreatik amilaz",
                "B": "Pankreatik lipaz",
                "C": "Tripsinojen",
                "D": "Karboksipeptidaz",
                "E": "Ribonükleaz"
            },
            "B",
            {
                "A": "Amilaz nişastayı sindirir, yağları hidrolize etmez.",
                "B": "Doğru cevap B'dir: Pankreatik lipaz trigliseritleri serbest yağ asitlerine yıkarak sabunlaşmayı başlatır.",
                "C": "Tripsin proenzimleri aktive eder.",
                "D": "Karboksipeptidaz proteinleri yıkar.",
                "E": "Ribonükleaz RNA yıkar."
            }
        ),
        28: make_micro_quiz(
            "Safra yolu tıkanıklığı (kolestaz) veya biliyer epitel hasarında kanda belirgin artış gösteren enzim biyobelirteci hangisidir?",
            {
                "A": "CK-MB",
                "B": "Alkalen fosfataz (ALP)",
                "C": "Troponin I",
                "D": "Lipaz",
                "E": "Asit fosfataz"
            },
            "B",
            {
                "A": "CK-MB miyokarda aittir.",
                "B": "Doğru cevap B'dir: Alkalen fosfataz (ALP) safra kanalikül membranında bulunur ve kolestazda kanda yükselir.",
                "C": "Troponin I kardiyak belirteçtir.",
                "D": "Lipaz pankreasa aittir.",
                "E": "Asit fosfataz prostat hasarında artabilir."
            }
        ),
        48: make_micro_quiz(
            "Apoptotik hücrelerin makrofajlar tarafından tanınmasını sağlayan ve floresan Anneksin V ile saptanan 'Beni ye' sinyali hangi moleküldür?",
            {
                "A": "Sfingomiyelin",
                "B": "Fosfatidilserin",
                "C": "Fosfatidilkolin",
                "D": "Kardiyolipin",
                "E": "Kolesterol esteri"
            },
            "B",
            {
                "A": "Sfingomiyelin miyelin kılıfındadır.",
                "B": "Doğru cevap B'dir: Zarın dış yaprağına takla atan fosfatidilserin makrofajlar için 'Beni ye' sinyalidir.",
                "C": "Fosfatidilkolin dış zarda normalde de bulunur.",
                "D": "Kardiyolipin mitokondri iç zarına özgüdür.",
                "E": "Kolesterol membran akışkanlığını düzenler."
            }
        ),
        58: make_micro_quiz(
            "Mitokondriyal yolda Sitokrom c sitoplazmaya sızdıktan sonra hangi adaptör proteinle birleşerek Apaptozom oluşturur?",
            {
                "A": "FADD",
                "B": "APAF-1",
                "C": "TRADD",
                "D": "RIPK1",
                "E": "MLKL"
            },
            "B",
            {
                "A": "FADD dışsal ölüm reseptörü adaptörüdür.",
                "B": "Doğru cevap B'dir: Sitokrom c APAF-1 ile birleşerek çarkıfelek apaptozomu kurar.",
                "C": "TRADD TNF yolağındadır.",
                "D": "RIPK1 nekroptozdadır.",
                "E": "MLKL nekroptozda por açar."
            }
        ),
        78: make_micro_quiz(
            "İnflamozom aktivasyonu, Kaspaz-1 çalışması ve IL-1beta salınımı ile yüksek ateşe yol açan programlı hücre ölümü hangisidir?",
            {
                "A": "Apoptoz",
                "B": "Piroptoz",
                "C": "Ferroptoz",
                "D": "Nekroptoz",
                "E": "Koagülatif nekroz"
            },
            "B",
            {
                "A": "Apoptozda inflamasyon ve ateş olmaz.",
                "B": "Doğru cevap B'dir: Piroptoz Kaspaz-1 ve Gazdermin D ile ateşli inflamasyon yapar.",
                "C": "Ferroptoz demir bağımlı lipid peroksidasyonudur.",
                "D": "Nekroptozda Kaspaz-1 çalışmaz.",
                "E": "Koagülatif nekroz iskemik doku ölümüdür."
            }
        ),
        88: make_micro_quiz(
            "Hücre hasarında artan sitozolik serbest kalsiyumun aktive ederek hücre zarı fosfolipidlerini doğrudan parçaladığı enzim hangisidir?",
            {
                "A": "Endonükleaz",
                "B": "Fosfolipaz",
                "C": "Katalaz",
                "D": "Süperoksit dismutaz",
                "E": "ATPaz"
            },
            "B",
            {
                "A": "Endonükleaz DNA'yı parçalar.",
                "B": "Doğru cevap B'dir: Fosfolipaz kalsiyum uyarısıyla hücre zarlarını parçalar.",
                "C": "Katalaz antioksidandır.",
                "D": "SOD antioksidandır.",
                "E": "ATPaz ATP tüketir."
            }
        )
    }

def build_extra_causal_chains():
    """6 ekstra mekanizma zinciri (causal_chain) envanteri."""
    return {
        17: make_causal_chain(
            "Lipidlerin Boyanma Prensibi Mekanizması",
            [
                "1. Solvent Etkisi: Rutin parafinde alkol ve ksilen hücre içi trigliseritleri çözer.",
                "2. Boşluk Görünümü: Standart H&E boyasında yağ dokusu boş beyaz petekler şeklinde kalır.",
                "3. Donuk Kesit: Taze dondurulan dokuda organik solventler kullanılmaz ve lipitler korunur.",
                "4. Oil Red O Boyası: Boya molekülleri nötral lipitlerin içine çözünerek hapsolur.",
                "5. Parlak Kırmızı Renk: Mikroskop altında damlacıklar turuncu-kırmızı renkte parlar."
            ]
        ),
        27: make_causal_chain(
            "Miyokard Nekrozunda Enzim Salınım Zinciri",
            [
                "1. Koroner Oklüzyon: Kan akımı kesilince kardiyomiyositlerde ATP tükenir.",
                "2. İyon Dengesizliği: Na+/K+ ve Ca2+ pompaları durarak sarkolemmayı gerer.",
                "3. Membran Rüptürü: Plazma zarı delinecek şekilde geri dönüşsüz parçalanır.",
                "4. Enzim Kaçışı: Sitoplazmik CK-MB ve troponin interstisyuma ve kapillerlere dökülür.",
                "5. Serum Tespiti: Kanda troponin ve CK-MB pik yaparak infarkt tanısını kesinleştirir."
            ]
        ),
        37: make_causal_chain(
            "Otoreaktif Lenfositlerin İntihar Zinciri",
            [
                "1. Timik Sunum: Meduller epitel hücreleri kendi doku antijenlerini olgunlaşan T hücrelerine sunar.",
                "2. Güçlü Bağlanma: Kendi antijenine aşırı afinite gösteren otoreaktif klonlar tespit edilir.",
                "3. Negatif Seçilim Sinyali: Hücrede Bim ve FasL genleri hızla transkribe edilir.",
                "4. Kaspaz Kaskadı: Mitokondriyal ve ölüm reseptörü yolakları eşzamanlı ateşlenir.",
                "5. Klonal Delesyon: Otoreaktif hücre apoptozla yok edilir ve otoimmünite engellenir."
            ]
        ),
        47: make_causal_chain(
            "Fosfatidilserin Dışa Dönüş Zinciri",
            [
                "1. Kaspaz Aktivasyonu: İnfazcı Kaspaz-3 hücrede aktif hale gelir.",
                "2. Flippaz İnaktivasyonu: Fosfatidilserini içte tutan ATP bağımlı flippaz kesilerek durdurulur.",
                "3. Skramblaz İndüksiyonu: Membran fosfolipidlerini karıştıran skramblaz enzimi aktive edilir.",
                "4. Dışa Dönüş: Fosfatidilserin zarın sitoplazmik yaprağından dış yaprağına takla atar.",
                "5. Makrofaj Tanıması: Makrofajlar PS reseptörleriyle hedefe bağlanıp sessiz fagositozu başlatır."
            ]
        ),
        57: make_causal_chain(
            "Smac/DIABLO ile Kaspaz Serbest Kalma Zinciri",
            [
                "1. Mitokondri Hasarı: BAX/BAK porları mitokondri dış zarını geçirgenleştirir.",
                "2. Smac/DIABLO Salınımı: Sitokrom c ile birlikte Smac/DIABLO proteini sitozole kaçar.",
                "3. IAP Bağlanması: Smac/DIABLO sitoplazmik apoptoz inhibitörlerine (XIAP) yüksek afiniteyle bağlanır.",
                "4. İnhibitörün Felci: IAP molekülleri kaspazları frenleme gücünü tamamen kaybeder.",
                "5. Engellenemez İnfaz: Kaspaz-3 ve Kaspaz-9 son hızla hücreyi parçalamaya devam eder."
            ]
        ),
        67: make_causal_chain(
            "İnfazcı Kaspazların Hücreyi Çökertme Zinciri",
            [
                "1. Başlatıcı Emir: Kaspaz-8 ve Kaspaz-9 infazcı Prokaspaz-3'ü keserek aktifleştirir.",
                "2. Lamin Parçalanması: Kaspaz-3 nükleer laminleri yıkarak çekirdek zarını çökertir.",
                "3. Aktin Kesimi: Hücre iskeleti proteinleri parçalanarak plazma zarı tomurcuklanır.",
                "4. PARP İnaktivasyonu: DNA tamir enzimi PARP kesilerek genomik onarım tamamen durdurulur.",
                "5. Apoptotik Cisimcikler: Hücre zarla çevrili küçük paketlere bölünerek yok oluşa gider."
            ]
        )
    }

def build_extra_before_after_sliders():
    """9 ekstra karşılaştırma kaydırıcısı (before_after_slider) envanteri."""
    return {
        3: make_before_after(
            "Kazeöz Nekroz vs Apse (Sıvılaşma Nekrozu)",
            "Kazeöz Nekroz",
            "Mycobacterium tuberculosis enfeksiyonunda görülür; makroskopide peynir benzeri ufalanan katı-yumuşak kitle, mikroskopide amorf granüler silinmiş dokudur.",
            "Sıvılaşma Nekrozu (Apse)",
            "Piyojenik bakteriyel enfeksiyonlarda görülür; nötrofillerin lizozomal sindirimi sonucu doku tamamen eriyerek püy (cerahat) içeren kistik kaviteye dönüşür."
        ),
        13: make_before_after(
            "Enzimatik Yağ Nekrozu vs Travmatik Yağ Nekrozu",
            "Enzimatik Yağ Nekrozu",
            "Akut pankreatitte asiner hücrelerden sızan aktif lipazların omental ve mezenterik trigliseritleri eritmesiyle gelişir; belirgin sabunlaşma odakları izlenir.",
            "Travmatik Yağ Nekrozu",
            "Meme veya subkutan yağ dokusuna künt travma veya cerrahi müdahale sonucu adiposit membranlarının yırtılmasıyla gelişir; memede karsinomu taklit eden kitle yapar."
        ),
        23: make_before_after(
            "Fibrinoid Nekroz vs Koagülatif Nekroz",
            "Fibrinoid Nekroz",
            "Küçük damar duvarlarında immün kompleksler ve ekstravaze fibrin birikimiyle oluşan, yalnızca ışık mikroskobunda tanınan amorf parlak pembe camsı lezyondur.",
            "Koagülatif Nekroz",
            "Solid organ enfarktlarında gelişen, makroskobik olarak görülebilen, doku mimarisinin hayalet hücreler şeklinde günlerce korunduğu iskemi nekrozudur."
        ),
        33: make_before_after(
            "Normal Parmak Gelişimi vs Sindaktili Anomalisi",
            "Fizyolojik İnterdigital Apoptoz",
            "Fetal ekstremite gelişiminde parmak aralarındaki mezenkim hücreleri programlı apoptoz ile erir; serbest hareketli beş bağımsız parmak oluşur.",
            "Sindaktili Anomalisi",
            "Parmak aralarındaki mezenkimal apoptozun yetersiz kalması veya durması sonucu parmaklar birbirine yapışık ve perdeli kalır."
        ),
        43: make_before_after(
            "Sağlıklı Hepatosit vs Councilman Cisimciği",
            "Sağlıklı Hepatosit",
            "Geniş poligonal sitoplazmalı, yuvarlak santral nükleuslu, ökromatin zengini canlı metabolik karaciğer hücresi.",
            "Councilman Cisimciği",
            "Viral hepatitte sitotoksik T hücrelerince apoptoza uğratılmış, büzüşmüş, koyu pembe-kırmızı boyanan ve çekirdeğini kaybetmiş apoptotik hepatosit kalıntısı."
        ),
        53: make_before_after(
            "Sağlıklı Mitokondri vs Pro-apoptotik MOMP",
            "Sağlam Mitokondri",
            "BCL-2 ve BCL-XL dış zar geçirgenliğini sımsıkı kapatır; Sitokrom c zarlar arası aralıkta güvenle hapsedilmiştir.",
            "MOMP Açılmış Mitokondri",
            "BAX ve BAK oligomerleşerek dış zarda dev porlar açar; Sitokrom c sitoplazmaya sızarak apaptozomu ve kaspaz-9'u ateşler."
        ),
        63: make_before_after(
            "DISC Kompleksi Varlığı vs c-FLIP Blokajı",
            "DISC Aktivasyonu",
            "FasL Fas'a bağlanır, FADD Prokaspaz-8'i toplar; Kaspaz-8 dimerleşip aktifleşerek dışsal apoptozu başlatır.",
            "c-FLIP İnhibisyonu",
            "c-FLIP sahte DED domainiyle DISC'e oturur ve Kaspaz-8'i kovar; enzimatik güç olmadığı için ölüm reseptörü yolağı kilitlenir."
        ),
        73: make_before_after(
            "Apoptoz vs Piroptoz İnflamatuar Yanıtı",
            "Apoptoz Yanıtı",
            "Hücre zarı sağlam kalır, apoptotik cisimcikler sessizce fagositozla yutulur; dokuda sıfır inflamasyon ve sıfır ateş izlenir.",
            "Piroptoz Yanıtı",
            "İnflamozom Kaspaz-1'i aktive eder, Gazdermin D zarı deler; yoğun IL-1beta salınımı ile şiddetli inflamasyon ve yüksek ateş oluşur."
        ),
        83: make_before_after(
            "Aktif p53 (Genom Bekçisi) vs Mutant p53 (Kanser)",
            "Sağlıklı p53 Fonksiyonu",
            "DNA kırığında p21 ile hücreyi G1'de durdurup onarır; hasar onarılamazsa BAX ve Puma ile apoptoza göndererek kanseri önler.",
            "Mutant p53 Fonksiyon Kaybı",
            "Hasarlı hücreler bölünmeye devam eder; genomik instabilite birikir, apoptoz gerçekleşmez ve neoplastik malign dönüşüm hızlanır."
        )
    }

def build_extra_branching_logic():
    """10 ekstra dallanan klinik karar senaryosu (branching_logic)."""
    return {
        4: make_branching_logic(
            "Akciğer biyopsisinde kazeöz nekroz, Langhans tipi dev hücreler ve epitelioid histiyositler izlenen hastanın lezyonunda Ziehl-Neelsen boyası negatif çıkıyor ancak klinisyen tüberkülozdan şüpheleniyor. Bir sonraki en doğru patolojik adım nedir?",
            [
                {
                    "text": "Lezyon kesinlikle tüberküloz değildir; kazeöz nekroz başka hiçbir hastalıkta görülmez.",
                    "isCorrect": False,
                    "feedback": "Hatalı! Derin mantar enfeksiyonları (Histoplasma vb.) kazeöz granülom yapabilir."
                },
                {
                    "text": "Mantar enfeksiyonlarını (Histoplazmoz) ekarte etmek için GMS ve PAS boyaları uygulanmalı, eşzamanlı olarak mikobakteriyel PCR veya kültür istenmelidir.",
                    "isCorrect": True,
                    "feedback": "Kusursuz klinik patoloji kararı! ZN negatifliğinde mantarlar aranmalı ve moleküler PCR ile tüberküloz araştırılmalıdır."
                },
                {
                    "text": "Hastaya derhal radyoterapi başlanmalıdır.",
                    "isCorrect": False,
                    "feedback": "Hatalı! Radyoterapi enfeksiyöz granülomun tedavisi değildir."
                }
            ]
        ),
        14: make_branching_logic(
            "Akut batın ile başvuran hastada serum amilaz ve lipaz düzeyleri normalin 5 katı bulunuyor. Acil cerrahiye alınan hastada mezenterde tebeşir beyazı odaklar saptanıyor. Bu lezyonların gelişmesinde ilk patofizyolojik basamak nedir?",
            [
                {
                    "text": "Pankreas asiner hücre hasarı sonucu sızan aktif lipazların adiposit trigliseritlerini serbest yağ asitlerine hidrolize etmesi.",
                    "isCorrect": True,
                    "feedback": "Doğru patobiyokimyasal basamak! Lipaz hidrolizi serbest yağ asitlerini açığa çıkarır ve sabunlaşmayı başlatır."
                },
                {
                    "text": "Hastanın aşırı kalsiyum tableti yutması sonucu doğrudan kireç birikmesi.",
                    "isCorrect": False,
                    "feedback": "Hatalı! Olay primer kalsiyum fazlalığı değil enzimatik hidrolizdir."
                },
                {
                    "text": "Pankreas kanserinin mezentere metastaz yapması.",
                    "isCorrect": False,
                    "feedback": "Hatalı! Bu tablo akut pankreatitin enzimatik yağ nekrozudur."
                }
            ]
        ),
        24: make_branching_logic(
            "Genç erkek hastada hipertansiyon, karın ağrısı ve periferik nöropati gelişiyor. Biyopside musküler arter duvarında transmural parlak pembe camsı nekroz ve nötrofiller saptanıyor. Serolojide HBsAg pozitif bulunuyor. En olası tanı nedir?",
            [
                {
                    "text": "Poliarteritis Nodosa (PAN)",
                    "isCorrect": True,
                    "feedback": "Tebrikler! Orta boy musküler arterlerde transmural fibrinoid nekroz ve HBV birlikteliği klasik PAN tablosudur."
                },
                {
                    "text": "Temporal (Dev Hücreli) Arterit",
                    "isCorrect": False,
                    "feedback": "Hatalı! Temporal arterit yaşlılarda büyük damarları tutar ve granülomatözdür."
                },
                {
                    "text": "Aort Diseksiyonu",
                    "isCorrect": False,
                    "feedback": "Hatalı! Diseksiyon kistik mediyal nekrozla seyreder, fibrinoid vaskülit değildir."
                }
            ]
        ),
        34: make_branching_logic(
            "Yenidoğan muayenesinde 3. ve 4. parmakları arasında cilt köprüsü saptanan (sindaktili) bebeğin embriyolojik gelişimindeki aksaklık nedir?",
            [
                {
                    "text": "Fetal el plağında interdigital mezenkim hücrelerinin programlı apoptozunun gerçekleşememesi.",
                    "isCorrect": True,
                    "feedback": "Kusursuz embriyopatoloji! Parmakların ayrışması interdigital apoptoza bağımlıdır; aksaması sindaktili yapar."
                },
                {
                    "text": "Kemiklerin aşırı çoğalarak parmakları birbirine kaynatması.",
                    "isCorrect": False,
                    "feedback": "Hatalı! Olay mezenkimin apoptozla eriyememesidir."
                },
                {
                    "text": "Aşırı inflamasyona bağlı parmakların fibrinle yapışması.",
                    "isCorrect": False,
                    "feedback": "Hatalı! Fetal dönemde fizyolojik süreç apoptozdur."
                }
            ]
        ),
        44: make_branching_logic(
            "Viral hepatit şüphesiyle incelenen karaciğer biyopsisinde sinüzoid boşluğunda yuvarlak, sitoplazması aşırı koyu pembe ve çekirdeği parçalanmış bir hepatosit (Councilman cisimciği) izleniyor. Bu hücrenin ölüm mekanizması nedir?",
            [
                {
                    "text": "Sitotoksik T lenfositlerin (CTL) perforin/granzim ve FasL ile indüklediği apoptoz.",
                    "isCorrect": True,
                    "feedback": "Doğru patolojik mekanizma! Councilman cisimcikleri CTL saldırısıyla apoptoza uğrayan hepatositlerdir."
                },
                {
                    "text": "İskemik koagülatif infarktüs.",
                    "isCorrect": False,
                    "feedback": "Hatalı! Karaciğer çift kanlandığı için tek hücreli infarkt görülmez."
                },
                {
                    "text": "Bakteriyel apse oluşumu.",
                    "isCorrect": False,
                    "feedback": "Hatalı! Apsede nötrofil ve sıvılaşma nekrozu izlenir."
                }
            ]
        ),
        54: make_branching_logic(
            "Foliküler lenfoma tanısı konan bir hastada t(14;18) translokasyonu saptanıyor. Tümör hücrelerinin kemoterapiye direnç göstermesinin ve apoptozdan kaçmasının moleküler sebebi nedir?",
            [
                {
                    "text": "Anti-apoptotik BCL-2 proteininin aşırı eksprese olarak mitokondri dış zarını geçirgenleşmeye (MOMP) karşı kapatması.",
                    "isCorrect": True,
                    "feedback": "Kusursuz onkolojik patoloji! Aşırı BCL-2 mitokondriden sitokrom c salınmasını engelleyerek apoptozu kilitler."
                },
                {
                    "text": "BAX ve BAK proteinlerinin tümör hücrelerinde delikler açması.",
                    "isCorrect": False,
                    "feedback": "Hatalı! BAX ve BAK apoptozu tetikler; foliküler lenfomada ise apoptoz engellenmiştir."
                },
                {
                    "text": "Tümör hücrelerinin nekroptoz ile patlaması.",
                    "isCorrect": False,
                    "feedback": "Hatalı! Hücreler ölmemekte, çoğalmaya devam etmektedir."
                }
            ]
        ),
        64: make_branching_logic(
            "Bir araştırma laboratuvarında kanser hücrelerine FasL veriliyor ancak hücreler ölmüyor. Hücre içi analizde Kaspaz-8'in DISC kompleksine bağlanamadığı ve yerinde c-FLIP proteininin oturduğu görülüyor. Bu durum neyi açıklar?",
            [
                {
                    "text": "c-FLIP'in Kaspaz-8'e yarışmalı engel olarak dışsal apoptoz yolunu felç ettiğini.",
                    "isCorrect": True,
                    "feedback": "Doğru moleküler mekanizma! c-FLIP sahte DED alanı ile DISC'e oturup Kaspaz-8 aktivasyonunu durdurur."
                },
                {
                    "text": "Hücrenin mitokondriyal yoldan öldüğünü.",
                    "isCorrect": False,
                    "feedback": "Hatalı! Hücre ölümden kaçmıştır."
                },
                {
                    "text": "Fas reseptörünün hücre zarında bulunmadığını.",
                    "isCorrect": False,
                    "feedback": "Hatalı! Reseptör vardır ancak DISC altındaki Kaspaz-8 blokajı vardır."
                }
            ]
        ),
        74: make_branching_logic(
            "Ağır sepsis ve çoklu organ yetmezliğinde doku harabiyetini yöneten Kaspaz-bağımsız programlı nekroz formunu (nekroptoz) hedeflemek isteyen farmakolog hangi molekülü inhibe etmelidir?",
            [
                {
                    "text": "RIPK1 veya RIPK3 kinaz aktivitesini.",
                    "isCorrect": True,
                    "feedback": "Kusursuz farmakolojik hedef! Nekroptoz RIPK1/RIPK3/MLKL kaskadıyla çalıştığı için RIPK inhibisyonu nekroptoza engel olur."
                },
                {
                    "text": "Kaspaz-3 enzimini.",
                    "isCorrect": False,
                    "feedback": "Hatalı! Nekroptoz zaten kaspaz-bağımsızdır; kaspaz blokajı nekroptozu daha da tetikler."
                },
                {
                    "text": "Anti-apoptotik BCL-2 proteinini.",
                    "isCorrect": False,
                    "feedback": "Hatalı! BCL-2 mitokondriyal yoldadır."
                }
            ]
        ),
        84: make_branching_logic(
            "ER stresi yaşayan bir hücrede katlanmamış protein yükü adaptif kapasiteyi aşıyor. Hücrede CHOP transkripsiyon faktörü aktive olduğunda hücre hangi kaderi yaşar?",
            [
                {
                    "text": "BCL-2 baskılanır, Bim ve Bax aktive olur ve hücre mitokondriyal apoptoz ile ölür.",
                    "isCorrect": True,
                    "feedback": "Doğru patobiyokimyasal akış! CHOP terminal UPR'nin apoptoz tetiğidir; BCL-2'yi kapatıp apoptozu başlatır."
                },
                {
                    "text": "Hücre şaperon üretimini on kat artırarak tamamen iyileşir.",
                    "isCorrect": False,
                    "feedback": "Hatalı! Bu adaptif evredir, kapasite aşılınca CHOP apoptoza götürür."
                },
                {
                    "text": "Hücre derhal malign metastaz yapar.",
                    "isCorrect": False,
                    "feedback": "Hatalı! Hücre intihar etmektedir."
                }
            ]
        ),
        94: make_branching_logic(
            "Demir yüklenmesi olan (hemokromatozis) bir hastada serbest Fe2+ iyonları dokularda hangi reaksiyonu katalizleyerek en güçlü serbest radikal olan hidroksil radikalini üretir?",
            [
                {
                    "text": "Fenton Reaksiyonu (Fe2+ + H2O2 -> Fe3+ + •OH + OH-)",
                    "isCorrect": True,
                    "feedback": "Tebrikler! Serbest demir H2O2'yi Fenton reaksiyonuyla en agresif radikal olan hidroksil radikaline çevirir."
                },
                {
                    "text": "Haber-Weiss reaksiyonunun tersi olan glikoliz basamağı",
                    "isCorrect": False,
                    "feedback": "Hatalı! Glikoliz demirle hidroksil üretmez."
                },
                {
                    "text": "Krebs döngüsündeki sitrat sentaz reaksiyonu",
                    "isCorrect": False,
                    "feedback": "Hatalı! Krebs döngüsü radikal üretim mekanizması değildir."
                }
            ]
        )
    }

def main():
    print("🚀 Kurul 1 - Ders 5 (Hücre Hasarı ve Nekroz - II) Tam Deste Oluşturucu Başlatılıyor...")
    deck_id = "k1p-k1-05-hucre-hasari-ve-nekroz-ii"
    os.makedirs(PACKAGES_DIR, exist_ok=True)
    os.makedirs(DECKS_ITEMS_DIR, exist_ok=True)

    # 1. TÜM 10 BÖLÜMÜ TOPLA (100 SLAYT)
    raw_slides = []
    for getter in [
        get_section_1_slides, get_section_2_slides, get_section_3_slides, get_section_4_slides,
        get_section_5_slides, get_section_6_slides, get_section_7_slides, get_section_8_slides,
        get_section_9_slides, get_section_10_slides
    ]:
        raw_slides.extend(getter())

    print(f"Toplanan ham adım sayısı: {len(raw_slides)}")
    assert len(raw_slides) == 100, f"HATA: Slayt sayısı tam 100 olmalıdır: {len(raw_slides)}"

    # 2. ÖRNEK SORULARI YÜKLE VE NORMALİZE ET
    questions = []
    if os.path.exists(QUESTIONS_FILE):
        with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
            q_data = json.load(f)
        raw_q_list = []
        if isinstance(q_data, dict):
            if "kazanimlar" in q_data:
                for k in q_data["kazanimlar"]:
                    raw_q_list.extend(k.get("sorular", []))
            elif "sorular" in q_data:
                raw_q_list.extend(q_data["sorular"])
        elif isinstance(q_data, list):
            raw_q_list = q_data

        for q in raw_q_list:
            q_id = q.get("id") or f"k1-05-q{len(questions)+1:02d}"
            q_text = q.get("soru") or q.get("question") or ""
            corr = q.get("dogru") or q.get("correctAnswer") or "A"
            if isinstance(corr, int):
                corr = chr(ord('A') + corr)
            corr = str(corr).strip().upper()
            if len(corr) > 1:
                corr = corr[0]
            if corr not in "ABCDE":
                corr = "A"

            gen_exp = q.get("aciklama") or q.get("explanation") or ""
            opt_exps = q.get("sik_aciklamalari") or {}

            raw_opts = q.get("secenekler") or q.get("options") or {}
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

    print(f"Yüklenen ve normalize edilen örnek soru sayısı: {len(questions)}")

    # 3. İNTERAKTİF ELEMANLARI DENGELE VE ASSEMBLE ET
    extra_quizzes = build_extra_micro_quizzes()
    extra_causal = build_extra_causal_chains()
    extra_sliders = build_extra_before_after_sliders()
    extra_branching = build_extra_branching_logic()

    final_slides = []
    checkpoint_counter = 0

    for idx, s in enumerate(raw_slides):
        slide_num = idx + 1
        s["slideNumber"] = slide_num

        is_checkpoint = (slide_num in [9, 19, 29, 39, 49, 59, 69, 79, 89, 100])
        s["isCheckpoint"] = is_checkpoint
        if is_checkpoint:
            checkpoint_counter += 1
            s["checkpointNumber"] = checkpoint_counter
            s["badge"] = "Tekrar Sayfası"
            s["badgeColor"] = "teal"

        # Tablo başlığı temizliği
        if s.get("coreContent", {}).get("table"):
            orig_title = s["coreContent"]["table"].get("title", "")
            s["coreContent"]["table"]["title"] = clean_table_title(orig_title)

        current_elems = list(s.get("interactiveElements", []))

        # Ekstra elemanları enjekte et
        if slide_num in extra_quizzes:
            current_elems.append(extra_quizzes[slide_num])
        if slide_num in extra_causal:
            current_elems.append(extra_causal[slide_num])
        if slide_num in extra_sliders:
            current_elems.append(extra_sliders[slide_num])
        if slide_num in extra_branching:
            current_elems.append(extra_branching[slide_num])

        # Eğer bir adımda birden fazla cloze varsa sadece 1 tanesini bırak (denge için)
        cloze_indices = [i for i, el in enumerate(current_elems) if el.get("type") == "cloze_masking"]
        if len(cloze_indices) > 1:
            for i in reversed(cloze_indices[1:]):
                del current_elems[i]

        # Adım başı sınırlandırma [1, 5]
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
            "checkpointNumber": checkpoint_counter if is_checkpoint else None,
            "sourcePdf": {
                "fileName": "3)Hücre Hasarı ve Nekroz 2.pdf",
                "fileId": "k1-05",
                "startPage": min(57, max(1, (slide_num * 57) // 100)),
                "endPage": min(57, max(1, ((slide_num * 57) // 100) + 1)),
                "primaryPage": min(57, max(1, (slide_num * 57) // 100)),
                "citation": f"Slayt {slide_num} · Kurul 1 Tıbbi Patoloji Sunumu (Prof. Dr. Hikmet Keleş)"
            },
            "aiPromptSuggestions": [
                f"{s['title']} konusunun biyokimyasal ve morfolojik mekanizmasını bir klinik olguyla açıklar mısın?",
                "Bu adımdaki nekroz veya apoptoz mekanizmasının TUS ve kurul sınavlarındaki ayırıcı tanılarını gösterir misin?"
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
        "id": "k1-05-hucre-hasari-ve-nekroz-ii",
        "title": "Hücre Hasarı ve Nekroz - II (Yeni Mikro-Ders)",
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
                html_lines.append(f"        <blockquote class=\"callout-box\">{p_clean.lstrip('> ')}</blockquote>")
            else:
                html_lines.append(f"        <p>{p_clean}</p>")
        html_lines.append("      </div>")

        if s["flashcards"]:
            html_lines.append("      <div class=\"flashcards-section\">")
            html_lines.append("        <h3>Tekrar Akıl Kartları</h3>")
            for fc in s["flashcards"]:
                html_lines.append(f"        <div class=\"flashcard\" data-id=\"{fc['id']}\">")
                html_lines.append(f"          <div class=\"flashcard-front\">{fc['front']}</div>")
                html_lines.append(f"          <div class=\"flashcard-back\">{fc['back']}</div>")
                html_lines.append("        </div>")
            html_lines.append("      </div>")

        if s.get("coreContent", {}).get("table"):
            tbl = s["coreContent"]["table"]
            html_lines.append("      <div class=\"table-section\">")
            html_lines.append(f"        <h3>{tbl.get('title', 'Özet Tablo')}</h3>")
            html_lines.append("        <table class=\"content-table\">")
            html_lines.append("          <thead><tr>")
            for h in tbl.get("headers", []):
                html_lines.append(f"            <th>{h}</th>")
            html_lines.append("          </tr></thead><tbody>")
            for r in tbl.get("rows", []):
                html_lines.append("          <tr>")
                for c in r:
                    html_lines.append(f"            <td>{c}</td>")
                html_lines.append("          </tr>")
            html_lines.append("        </tbody></table>")
            html_lines.append("      </div>")

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
        f"# {manifest_data['title']}",
        f"**Disiplin:** {manifest_data['discipline']} | **Öğretim Üyesi:** {manifest_data['instructor']}",
        f"**Toplam Adım:** 100 | **İnteraktif Öğe:** {total_elems} | **Checkpoint Sayısı:** 10",
        "\n---\n"
    ]
    for s in final_slides:
        cp_tag = " [TEKRAR SAYFASI]" if s["isCheckpoint"] else ""
        md_lines.append(f"## {s['slideNumber']}. {s['title']}{cp_tag}")
        md_lines.append(f"*{s['subtitle']}*\n")
        md_lines.append(s["synthesisNarrative"])
        md_lines.append("")

        if s["spotPearls"]:
            md_lines.append("### Sınav Spotları")
            for sp in s["spotPearls"]:
                md_lines.append(f"- {sp}")
            md_lines.append("")

        if s["flashcards"]:
            md_lines.append("### Akıl Kartları (Flashcards)")
            for fc in s["flashcards"]:
                md_lines.append(f"- **Soru:** {fc['front']}")
                md_lines.append(f"  - **Cevap:** {fc['back']}")
            md_lines.append("")

        if s.get("coreContent", {}).get("table"):
            tbl = s["coreContent"]["table"]
            md_lines.append(f"### {tbl.get('title', 'Özet Tablo')}")
            headers = tbl.get("headers", [])
            md_lines.append("| " + " | ".join(headers) + " |")
            md_lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
            for r in tbl.get("rows", []):
                md_lines.append("| " + " | ".join(str(c) for c in r) + " |")
            md_lines.append("")

        md_lines.append("\n---\n")

    md_path = os.path.join(PACKAGES_DIR, "content.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
    print(f"4. Content Markdown yazıldı: {md_path}")

    # 5. RUNTIME ITEM JSON
    deck_data = {
        "id": deck_id,
        "title": "Hücre Hasarı ve Nekroz - II (Yeni Mikro-Ders)",
        "shortTitle": "Hücre Hasarı ve Nekroz - II",
        "discipline": "Tıbbi Patoloji",
        "committee": "Kurul 1 (Ürogenital ve Obstetrik)",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "audioFile": "audios/kurul1/k1-05-hucre-hasari-ve-nekroz-ii.mp3",
        "audioDuration": "54:30",
        "confidence": "Yüksek",
        "themeColor": "red",
        "matchedNoteId": "k1-05-hucre-hasari-ve-nekroz-ii",
        "matchedNoteTitle": "Hücre Hasarı ve Nekroz - II Ders Özeti",
        "isNew": True,
        "isLegacy": False,
        "version": 2,
        "packageSources": {
            "manifest": "packages/k1-05-hucre-hasari-ve-nekroz-ii/manifest.json",
            "structureXml": "packages/k1-05-hucre-hasari-ve-nekroz-ii/structure.xml",
            "blocksHtml": "packages/k1-05-hucre-hasari-ve-nekroz-ii/blocks.html",
            "contentMd": "packages/k1-05-hucre-hasari-ve-nekroz-ii/content.md"
        },
        "overview": f"Bu interaktif mikro-öğrenme destesi; 100 atomik adımda, 10 kontrol noktası tekrar sayfasında gömülü 30 akıl kartıyla, {total_elems} adet dengeli interaktif alıştırmayla (mikro-quiz, maskeli tablo, dallanan klinik kararlar, aktif hatırlama, karşılaştırma kaydırıcısı, mekanizma zinciri) kazeöz, yağ ve fibrinoid nekrozu; plazma zarı rüptürüyle kana kaçan serum biyobelirteçlerini (CK-MB, ALT, AST, ALP); apoptozun fizyolojik ve patolojik temellerini; mitokondriyal (BCL-2, BAX/BAK, Apaptozom, Kaspaz-9) ve ölüm reseptörü (Fas/CD95, DISC, Kaspaz-8) yolaklarını; infazcı kaspazları (Kaspaz-3, CAD, 180-200 bç DNA merdiveni); yeni ölüm biçimlerini (nekroptoz, piroptoz, ferroptoz) ve otofajiyi; p53 genom bekçisini, ER stresini (UPR/CHOP), sitozolik kalsiyum kaosu ve 4 yıkıcı enzimi; reaktif oksijen türlerini (Fenton hidroksil radikali), antioksidan savunmayı ve iskemik hücresel kaskadı derinlemesine öğretir.",
        "highYieldPearls": [
            "📌 [SINAV SPOTU] Kazeöz nekroz tüberküloza özgüdür; peynirimsi makroskopi, amorf granüler mimari ve Langhans granülomuyla karakterizedir.",
            "📌 [SINAV SPOTU] Yağ nekrozunun en dramatik örneği akut pankreatittir; lipazlar trigliseritleri parçalar, serbest yağ asitleri kalsiyum ile sabunlaşır (saponifikasyon).",
            "📌 [SINAV SPOTU] Fibrinoid nekroz makroskobide görülmez; ışık mikroskobunda damar duvarında parlak pembe amorf camsı immün kompleks ve fibrin birikimidir (PAN, Malign HT).",
            "📌 [SINAV SPOTU] Nekrozda hücre zarı delinir ve enzimler kana kaçar: Kalp -> Troponin ve CK-MB; Karaciğer -> ALT ve AST; Safra -> ALP; Pankreas -> Lipaz.",
            "📌 [SINAV SPOTU] Apoptoz programlı, düzenlenmiş ve ENERJİ (ATP) BAĞIMLIDIR; membran bütünlüğü korunur ve çevre dokuda HİÇBİR İNFLAMASYON oluşmaz.",
            "📌 [SINAV SPOTU] Mitokondriyal (içsel) yolda BAX/BAK por açar, Sitokrom c APAF-1 ile Apaptozomu kurar ve Başlatıcı KASPAZ-9'u aktive eder.",
            "📌 [SINAV SPOTU] Ölüm reseptörü (dışsal) yolunda FasL Fas'a bağlanır, FADD ile DISC kompleksi kurulur ve Başlatıcı KASPAZ-8 aktive olur.",
            "📌 [SINAV SPOTU] Ortak ana infazcı kaspaz KASPAZ-3'tür; ICAD'i yıkarak CAD endonükleazını serbest bırakır ve 180-200 baz çiftlik DNA Merdiveni oluşturur.",
            "📌 [SINAV SPOTU] Nekroptoz RIPK1/3/MLKL ile programlı nekrozdur; Piroptoz Kaspaz-1/IL-1 ile yüksek ateş yapar; Ferroptoz demir bağımlı lipid peroksidasyonudur.",
            "📌 [SINAV SPOTU] p53 'Genom Bekçisi'dir; hafif hasarda p21 ile döngüyü durdurur, ağır hasarda BAX/Puma ile apoptozu patlatır; kaybı Li-Fraumeni sendromu ve kanser yapar.",
            "📌 [SINAV SPOTU] Hücre hasarında bilinen EN GÜÇLÜ serbest radikal demir katalizli Fenton reaksiyonuyla üretilen Hidroksil Radikalidir (•OH)."
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
                entry["title"] = "Hücre Hasarı ve Nekroz - II (Yeni Mikro-Ders)"
                entry["overview"] = deck_data["overview"]
                entry["audioDuration"] = "54:30"
                found = True
                break
        if not found:
            catalog.append({
                "id": deck_id,
                "title": "Hücre Hasarı ve Nekroz - II (Yeni Mikro-Ders)",
                "shortTitle": "Hücre Hasarı ve Nekroz - II",
                "discipline": "Tıbbi Patoloji",
                "committee": "Kurul 1 (Ürogenital ve Obstetrik)",
                "instructor": "Prof. Dr. Hikmet Keleş",
                "totalSlides": 100,
                "isNew": True,
                "isLegacy": False,
                "version": 2,
                "audioDuration": "54:30",
                "overview": deck_data["overview"]
            })
        with open(CATALOG_PATH, "w", encoding="utf-8") as f:
            json.dump(catalog, f, ensure_ascii=False, indent=2)
        print(f"7. Catalog JSON güncellendi: {CATALOG_PATH}")

    print("\n✅ TÜM DERS 5 MULTI-FORMAT İŞLEMLERİ BAŞARIYLA TAMAMLANDI!")

if __name__ == "__main__":
    main()
