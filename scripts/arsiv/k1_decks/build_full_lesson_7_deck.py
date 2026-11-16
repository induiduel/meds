#!/usr/bin/env python3
"""
Kurul 1 - Ders 7: Hücre İçi Birikimler ve Kalsifikasyonlar (Prof. Dr. Hikmet Keleş)
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

from scripts.k1_07_deck_data.helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)
from scripts.k1_07_deck_data.section_1 import get_section_1_slides
from scripts.k1_07_deck_data.section_2 import get_section_2_slides
from scripts.k1_07_deck_data.section_3 import get_section_3_slides
from scripts.k1_07_deck_data.section_4 import get_section_4_slides
from scripts.k1_07_deck_data.section_5 import get_section_5_slides
from scripts.k1_07_deck_data.section_6 import get_section_6_slides
from scripts.k1_07_deck_data.section_7 import get_section_7_slides
from scripts.k1_07_deck_data.section_8 import get_section_8_slides
from scripts.k1_07_deck_data.section_9 import get_section_9_slides
from scripts.k1_07_deck_data.section_10 import get_section_10_slides

# Dosya yolları
QUESTIONS_FILE = os.path.join(BASE_DIR, "meds/src/data/ornek_sorular/k1/k1-07-hucre-ici-birikimler-ve-kalsifikasyonlar.json")
PACKAGE_DIR = os.path.join(BASE_DIR, "meds/src/data/decks/packages/k1-07-hucre-ici-birikimler-ve-kalsifikasyonlar")
DECKS_ITEMS_DIR = os.path.join(BASE_DIR, "meds/src/data/decks/items")
INTERACTIVE_DECKS_PATH = os.path.join(BASE_DIR, "meds/src/data/interactive_learning_decks.json")
CATALOG_PATH = os.path.join(BASE_DIR, "meds/src/data/decks/catalog.json")

def fold(s):
    return str(s or '').lower().replace('ı', 'i').replace('İ', 'i')

def leaks(hint: str, answer: str) -> bool:
    """İpucu cevap kelimelerinden birini sızdırıyor mu denetler (validator ile birebir aynı)."""
    if not hint or not answer:
        return False
    import re
    h = fold(hint)
    return any((w[:5] if len(w) > 5 else w) in h for w in re.findall(r'[\wçğıöşü%.,-]+', fold(answer)) if len(w) >= 3 or re.search(r'\d', w))

def sanitize_hint(hint: str, answer: str, fallback="İlgili patofizyolojik kavramı hatırlayınız") -> str:
    if not hint or leaks(hint, answer):
        return fallback
    return hint

def clean_table_title(title: str) -> str:
    t = title
    for junk in [
        "İnteraktif Karşılaştırma Tablosu", "Karşılaştırma Tablosu",
        "İnteraktif Tablo", "Tablo:", "Özet Tablo", "Özet:", "Kritik Tablo"
    ]:
        t = t.replace(junk, "").strip()
    t = t.rstrip(":-· ")
    return t if len(t) > 2 else "Klinik Özet Tablosu"

def build_extra_micro_quizzes():
    """4 ekstra mikro soru (micro_quiz) envanteri."""
    return {
        3: make_micro_quiz(
            "Hepatositlerde normal endojen trigliserid birikiminin temel nedeni olan mekanizma hangisidir?",
            {
                "A": "Eksojen inorganik partiküllerin fagositozu",
                "B": "Normal endojen maddenin sentezinin sekresyon veya katabolizmayı aşması",
                "C": "Lizozomal sfingomiyelinaz enzim mutasyonu",
                "D": "SERPINA1 geninde katlanma defekti",
                "E": "Otoimmün kompleman birikimi"
            },
            "B",
            {
                "A": "Eksojen partikül antrakozistir.",
                "B": "Doğru cevap B'dir: Normal endojen maddenin yetersiz uzaklaştırılması steatozun temelidir.",
                "C": "Sfingomiyelinaz Niemann-Pick'tir.",
                "D": "SERPINA1 alfa-1 antitripsindir.",
                "E": "Kompleman immün kompleks hasarıdır."
            }
        ),
        23: make_micro_quiz(
            "Aterosklerozda makrofajların köpük hücreye dönüşmesinde oxLDL'yi durmaksızın yutan reseptör hangisidir?",
            {
                "A": "Klasik LDL reseptörü",
                "B": "Çöpçü (scavenger) reseptörler (SR-A, CD36)",
                "C": "VLDL reseptörü",
                "D": "Transferrin reseptörü",
                "E": "Megalocilin reseptörü"
            },
            "B",
            {
                "A": "Klasik LDL reseptörü negatif geri bildirimle baskılanır.",
                "B": "Doğru cevap B'dir: Çöpçü reseptörlerde down-regülasyon yoktur, sınırsız lipid alırlar.",
                "C": "VLDL primer rol oynamaz.",
                "D": "Transferrin demir bağlar.",
                "E": "Megalocilin bulunmaz."
            }
        ),
        53: make_micro_quiz(
            "Diyabetik ketoasidozda böbrek proksimal tübül hücrelerinde glikojen birikmesiyle oluşan lezyon hangisidir?",
            {
                "A": "Mallory-Denk cisimciği",
                "B": "Armanni-Ebstein lezyonu",
                "C": "Russell cisimciği",
                "D": "Psammom cisimciği",
                "E": "Kimmelstiel-Wilson nodülü"
            },
            "B",
            {
                "A": "Mallory-Denk hepatositte sitokeratindir.",
                "B": "Doğru cevap B'dir: Armanni-Ebstein tübül epitelinde glikojen birikimidir.",
                "C": "Russell cisimciği plazma hücresindedir.",
                "D": "Psammom konsantrik kalsiyumdur.",
                "E": "Kimmelstiel-Wilson glomerüler nodüler sklerozdur."
            }
        ),
        83: make_micro_quiz(
            "Distrofik kalsifikasyonda hücre içi ilk kristal çekirdeklenmesinin başladığı organel hangisidir?",
            {
                "A": "Peroksizom",
                "B": "Nekrotik hücre mitokondrisi",
                "C": "Golgi cisimciği",
                "D": "Granülsüz ER",
                "E": "Sentrozom"
            },
            "B",
            {
                "A": "Peroksizom hidrojen peroksit metabolize eder.",
                "B": "Doğru cevap B'dir: Distrofik kalsifikasyon hücre içinde nekrotik mitokondrilerde başlar.",
                "C": "Golgi salgı paketler.",
                "D": "Granülsüz ER lipid sentezler.",
                "E": "Sentrozom mikrotübül merkezidir."
            }
        )
    }

def build_extra_causal_chains():
    """6 ekstra mekanizma zinciri (causal_chain) envanteri."""
    return {
        8: make_causal_chain(
            "Kolesteroloziste Köpük Hücre Göllenme Zinciri",
            [
                "1. Aşırı Safrasal Kolesterol: Safrada kolesterol konsantrasyonu aşırı artar.",
                "2. Mukozal Difüzyon: Kolesterol epitelden lamina propria bağ dokusuna sızar.",
                "3. Makrofaj Fagositozu: Lamina propriadaki histiositler sterolleri içine alıp depolar.",
                "4. Çilek Manzarası: Sarı lipid benekleri kırmızı mukoza zemininde çilek görünümü oluşturur."
            ]
        ),
        28: make_causal_chain(
            "Tendon Ksantomu Oluşum Basamakları",
            [
                "1. Ağır Hiperkolesterolemi: LDL reseptör mutasyonuyla plazma LDL'si tavan yapar.",
                "2. Tendon Sızıntısı: Mekanik sürtünmeye uğrayan Aşil tendonu kılıfına lipidler sızar.",
                "3. Doku Makrofajı Fagositozu: Doku histiositleri kolesterolü yutarak dev köpük hücreler kurar.",
                "4. Nodüler Kitle: Kolesterol dolu makrofajlar ve fibröz stroma sert nodüler tümörler meydana getirir."
            ]
        ),
        38: make_causal_chain(
            "Alzheimer Hastalığında Nörofibriler Yumak Zinciri",
            [
                "1. Mikrotübül Kararsızlığı: Kinaz aktivitesi Tau proteinini aşırı fosforiller.",
                "2. Çözünme ve Bükülme: Hiperfosforile Tau mikrotübüllerden ayrılarak bükülür.",
                "3. Helikal Filamentler: Tau polimerleri eşleşmiş helikal filamentler (PHF) oluşturur.",
                "4. Nöronal Kilitlenme: Nörofibriler yumaklar aksonal taşımayı felç ederek nöronu öldürür."
            ]
        ),
        48: make_causal_chain(
            "α1-Antitripsin Polimerizasyonu ve Karaciğer Hasarı",
            [
                "1. SERPINA1 Mutasyonu: PiZZ mutasyonu protein katlanma döngüsünü bozar.",
                "2. ER Hapsi: Mutant AAT molekülleri hepatosit granüllü ER'sinde polimerleşir.",
                "3. Şaperon Tükenmesi: Aşırı agregat ER şaperonlarını kilitler ve kronik UPR başlatır.",
                "4. Hepatosit Sirozu: Devam eden ER stresi apoptozu ve perisinüzoidal fibrozisi tetikler."
            ]
        ),
        68: make_causal_chain(
            "Melanin Biyosentezi ve DNA Koruma Zinciri",
            [
                "1. Tirozinaz Aktivasyonu: Melanositler tirozin amino asidini DOPA üzerinden melanine çevirir.",
                "2. Melanozom Paketlemesi: Pigment özelleşmiş melanozom vezikülleri içinde yoğunlaştırılır.",
                "3. Keratinosit Aktarımı: Melanosit dendritleri melanozomları bazal keratinositlere verir.",
                "4. Nükleer Şemsiye: Keratinositler melanini çekirdek üzerine yerleştirerek DNA'yı UV'den korur."
            ]
        ),
        88: make_causal_chain(
            "Psammom Cisimciği Konsantrik Tabakalanma Zinciri",
            [
                "1. Hücresel Ölüm: Tek bir papiller tümör hücresi apoptoz veya nekroza gider.",
                "2. Membran Nükleasyonu: Ölü hücre zarı kalsiyum fosfat kristalleri için nidus olur.",
                "3. Lameller Büyüme: Kalsiyum tuzları soğan zarı gibi iç içe katmanlar halinde çöker.",
                "4. Taşlaşmış Küre: Konsantrik bazofilik psammom cisimciği mikroskopta kalıcı iz bırakır."
            ]
        )
    }

def build_extra_before_after_sliders():
    """2 ekstra karşılaştırma kaydırıcısı (before_after_slider) envanteri."""
    return {
        13: make_before_after(
            "Alkol Öncesi Hepatosit vs Alkol Sonrası Steatoz",
            "Fizyolojik Hepatosit",
            "Düşük NADH/NAD+ oranı, aktif mitokondriyal beta-oksidasyon ve düzenli VLDL salınımı mevcuttur.",
            "Alkolik Hepatosit (Steatoz)",
            "Yüksek NADH/NAD+ oranı, kilitlenmiş mitokondriyal yağ asidi oksidasyonu ve sitoplazmada devasa trigliserid vakuolleri mevcuttur."
        ),
        63: make_before_after(
            "Normal Akciğer vs Antrakotik Akciğer",
            "Normal Akciğer",
            "Pembe, süngerimsi parankim, berrak alveol boşlukları ve pigmentsiz hiler lenf düğümleri içerir.",
            "Antrakotik Akciğer",
            "Siyah çizgilenmeler içeren alacalı parankim, karbon dolu toz hücreleri ve kömür karası hiler lenf nodları içerir."
        )
    }

def build_extra_branching_logic():
    """12 ekstra klinik dallanan karar senaryosu (branching_logic) envanteri."""
    return {
        2: make_branching_logic(
            "Sitoplazmasında vakuol birikimi izlenen bir doku kesitinde patolog birikintinin trigliserid mi yoksa glikojen mi olduğunu hızla netleştirmek istemektedir.",
            [
                {
                    "text": "Formalin fiksasyonlu H&E kesitine doğrudan bakılması yeterlidir çünkü trigliserid mor boyanır.",
                    "isCorrect": False,
                    "feedback": "H&E takibinde hem lipid hem glikojen eridiği için ikisi de boş vakuol bırakır, mor boyanmaz."
                },
                {
                    "text": "Dondurulmuş kesitte Oil Red O (veya Sudan) boyası ile PAS-diyastaz testi birlikte uygulanmalıdır.",
                    "isCorrect": True,
                    "feedback": "Doğru yaklaşım! Dondurulmuş kesitte Oil Red O trigliseridi parlak kırmızı boyarken, PAS-diyastaz glikojeni kanıtlar."
                }
            ]
        ),
        12: make_branching_logic(
            "Rutin biyokimya taramasında hafif ALT/AST yüksekliği saptanan obez bir hastada batın USG'de karaciğerde parlak ekojenite artışı izleniyor. Karaciğer parankiminde ne tür bir hücresel birikim düşünülmelidir?",
            [
                {
                    "text": "Hepatosit granüllü ER'sinde aşırı mutant alfa-1 antitripsin birikimi",
                    "isCorrect": False,
                    "feedback": "Obezitede primer patoloji alfa-1 antitripsin mutasyonu değil, serbest yağ asidi yüklenmesidir."
                },
                {
                    "text": "İnsülin direncine bağlı hepatosit sitoplazmasında aşırı trigliserid birikimi (steatoz)",
                    "isCorrect": True,
                    "feedback": "Kusursuz! Obezitede artan serbest yağ asidi akışı karaciğerde trigliserid depolanması (steatoz) oluşturur."
                }
            ]
        ),
        16: make_branching_logic(
            "Ağır kronik anemi nedeniyle takip edilen bir hastanın kalbinde makroskopik olarak sarı yağlı çizgiler ile kırmızı kas liflerinin ardışık dizilimi izleniyor. Bu patolojik tablonun nedeni nedir?",
            [
                {
                    "text": "Kronik hipoksiye bağlı kardiyomiyositlerde mitokondriyal yağ asidi oksidasyon bozukluğu ve steatoz",
                    "isCorrect": True,
                    "feedback": "Harika! Hipoksi mitokondriyal beta-oksidasyonu bozar ve kaplan derisi (tigroid kalp) manzarası yaratır."
                },
                {
                    "text": "Epikardiyal yağın miyokard lifleri arasına kontrolsüz neoplastik invazyonu",
                    "isCorrect": False,
                    "feedback": "Tigroid kalp neoplastik infiltrasyon değil, kardiyomiyositlerin hipoksik steatozudur."
                }
            ]
        ),
        22: make_branching_logic(
            "Koroner arter intimasına sızan LDL partikülleri makrofajlar tarafından sınırsızca fagosite edilmektedir. Makrofajın bu sınırsız lipid alımını durduramamasının nedeni nedir?",
            [
                {
                    "text": "Çöpçü (scavenger) reseptörlerin hücre içi kolesterol artsa bile down-regüle olmaması",
                    "isCorrect": True,
                    "feedback": "Tebrikler! Çöpçü reseptörler negatif geri bildirim mekanizmasına sahip değildir, köpük hücreyi oluşturur."
                },
                {
                    "text": "Klasik LDL reseptörlerinin aşırı kalsiyum salgılayarak zarı delmesi",
                    "isCorrect": False,
                    "feedback": "Klasik LDL reseptörü kolesterol artınca kapanır; sorumlu olan çöpçü reseptörlerdir."
                }
            ]
        ),
        32: make_branching_logic(
            "Nefrotik sendromlu bir hastanın böbrek biyopsisinde proksimal tübül hücre sitoplazmasında parlak pembe yuvarlak damlacıklar izleniyor. Glomerül hasarı tedavi edildiğinde bu damlacıkların akıbeti ne olur?",
            [
                {
                    "text": "Geri dönüşsüz koagülatif nekroza yol açarak tübülün tamamen kalsifiye olmasına neden olur.",
                    "isCorrect": False,
                    "feedback": "Protein reabsorpsiyon damlacıkları nekroz yapmaz, tamamen geri dönüşümlü bir adaptasyondur."
                },
                {
                    "text": "Proteinüri düzeldiğinde lizozomal enzimlerle amino asitlere sindirilerek tamamen kaybolur.",
                    "isCorrect": True,
                    "feedback": "Doğru! Proksimal tübül damlacıkları tamamen reversibldir, protein kaçağı kesilince kaybolur."
                }
            ]
        ),
        36: make_branching_logic(
            "Alkolik hepatit tanılı bir hastanın karaciğer biyopsisinde dejenere hepatosit sitoplazmasında kıvrıntılı eozinofilik Mallory-Denk inklüzyonları görülüyor. Bu inklüzyonun temel bileşeni nedir?",
            [
                {
                    "text": "Ubikitine bağlanmış sitokeratin ara filamentleri",
                    "isCorrect": True,
                    "feedback": "Doğru! Mallory-Denk cisimcikleri sitokeratin 8/18 ara filamentleri ve ubikitinden oluşur."
                },
                {
                    "text": "Granüllü ER sisternalarında birikmiş monoklonal immünoglobulinler",
                    "isCorrect": False,
                    "feedback": "Granüllü ER'deki immünoglobulin Russell cisimciğidir, Mallory-Denk değildir."
                }
            ]
        ),
        42: make_branching_logic(
            "Hücrede yanlış katlanmış proteinlerin aşırı birikmesi sonucu tetiklenen açılmamış protein yanıtı (UPR) stresi çözemezse hücre hangi yolağı aktive eder?",
            [
                {
                    "text": "CHOP transkripsiyon faktörü üzerinden pro-apoptotik proteinleri aktive ederek apoptozu başlatır.",
                    "isCorrect": True,
                    "feedback": "Mükemmel! Kronik ağır ER stresi CHOP indüksiyonu ile hücreyi intihara (apoptoza) sürükler."
                },
                {
                    "text": "Mitoz bölünmeyi hızlandırarak mutant proteini kız hücrelere eşit paylaştırır.",
                    "isCorrect": False,
                    "feedback": "ER stresi mitozu durdurur; çözülemezse apoptoz tetiklenir."
                }
            ]
        ),
        52: make_branching_logic(
            "Bir patolog doku kesitinde PAS ile pozitif (eflatun) boyanan bir vakuolün glikojen mi yoksa müsin/alfa-1 antitripsin mi olduğunu kesinleştirmek istemektedir.",
            [
                {
                    "text": "Dokuya amilaz (diyastaz) enzimi uygulanmalıdır; boyanma kayboluyorsa glikojendir.",
                    "isCorrect": True,
                    "feedback": "Doğru karar! Glikojen diyastaza duyarlıdır ve erir; müsin ve AAT ise diyastaza dirençlidir."
                },
                {
                    "text": "Dokuya Prusya mavisi uygulanmalıdır; maviye boyanıyorsa glikojendir.",
                    "isCorrect": False,
                    "feedback": "Prusya mavisi demir (hemosiderin) boyasıdır, glikojeni göstermez."
                }
            ]
        ),
        62: make_branching_logic(
            "Madenci bir hastanın akciğer otopsisinde hiler lenf düğümlerinin simsiyah olduğu görülüyor. Mikroskopta makrofajların içinde siyah granüller saptanıyor. Bu pigmentin temel biyolojik özelliği nedir?",
            [
                {
                    "text": "Kimyasal olarak inert bir eksojen karbon partikülüdür; dokuda enzimlerle sindirilemez.",
                    "isCorrect": True,
                    "feedback": "Doğru! Karbon partikülleri sindirilemeyen eksojen maddelerdir ve makrofajlarda kalıcı kalır."
                },
                {
                    "text": "Tirozinaz enzimiyle aşırı sentezlenmiş endojen melanin polimeridir.",
                    "isCorrect": False,
                    "feedback": "Akciğerdeki siyah pigment antrakozisdir (karbon); derideki melanin değildir."
                }
            ]
        ),
        72: make_branching_logic(
            "Karaciğer biyopsisinde hepatositlerde altın-pas kahverengisi kaba granüller saptanıyor. Patolog pigmentin demir mi yoksa lipofusin mi olduğunu kanıtlamak için hangi testi yapmalıdır?",
            [
                {
                    "text": "Prusya mavisi (Perls) boyası uygulamalıdır; demir içeriyorsa parlak mavi boyanır.",
                    "isCorrect": True,
                    "feedback": "Harika! Prusya mavisi hemosiderini masmavi boyayarak lipofusin ve melaninden kesin ayırır."
                },
                {
                    "text": "Kongo kırmızısı boyası uygulamalıdır; elma yeşili röfle veriyorsa demirdir.",
                    "isCorrect": False,
                    "feedback": "Kongo kırmızısı amiloid boyasıdır, demirle ilgisi yoktur."
                }
            ]
        ),
        82: make_branching_logic(
            "70 yaşında aort kapağında taş gibi sert kalsiyum nodülleri nedeniyle kapak replasmanı yapılan hastada kan biyokimyasında kalsiyum 9.4 mg/dL (normal) bulunuyor. Bu kalsifikasyonun tipi nedir?",
            [
                {
                    "text": "Distrofik kalsifikasyon: Serum kalsiyumu normal iken mekanik hasarlı kapakta gelişmiştir.",
                    "isCorrect": True,
                    "feedback": "Doğru! Normokalsemi zemininde hasarlı dokuda gelişen kireçlenme distrofik kalsifikasyondur."
                },
                {
                    "text": "Metastatik kalsifikasyon: Kanser metastazına bağlı gelişmiştir.",
                    "isCorrect": False,
                    "feedback": "Metastatik kalsifikasyonda hiperkalsemi şarttır; bu hastada kalsiyum normaldir."
                }
            ]
        ),
        92: make_branching_logic(
            "Paratiroid adenomu nedeniyle serum kalsiyumu 14.2 mg/dL ölçülen bir hastanın akciğer ve mide mukozasında kalsiyum çökmesi saptanıyor. Bu patolojik mineralizasyonun sınıfı nedir?",
            [
                {
                    "text": "Metastatik kalsifikasyon: Hiperkalsemi zemininde normal dokularda gelişmiştir.",
                    "isCorrect": True,
                    "feedback": "Kusursuz! Yüksek serum kalsiyumu nedeniyle normal dokularda gelişen çöküntü metastatik kalsifikasyondur."
                },
                {
                    "text": "Distrofik kalsifikasyon: Mide ve akciğerde kazeöz nekroz gelişmiştir.",
                    "isCorrect": False,
                    "feedback": "Nekroz olmadan hiperkalsemiyle oluşan yaygın çökme metastatik tiptir."
                }
            ]
        )
    }

def build_extra_tables():
    """10 ekstra interaktif maskeli tablo (interactive_table) envanteri."""
    return {
        4: make_table(
            ["Mekanizma Tipi", "Hücresel Örnek", "Biriken Madde Türü"],
            [
                [("Mekanizma 1 (Yetersiz Klirens)", False, ""), ("Karaciğer Steatozu", False, ""), ("Normal Trigliserid", True, "Hepatositte göllenen nötral lipid")],
                [("Mekanizma 2 (Anormal Endojen)", False, ""), ("α1-Antitripsin Eksikliği", False, ""), ("Mutant AAT Proteini", True, "SERPINA1 gen ürünü katlanmamış polipeptit")],
                [("Mekanizma 3 (Eksojen Madde)", False, ""), ("Akciğer Antrakozisi", False, ""), ("Karbon Partikülleri", True, "Solunumla alınan sindirilemeyen inorganik toz")],
                [("Mekanizma 4 (Lizozomal Enzim Defekti)", False, ""), ("Tay-Sachs Hastalığı", False, ""), ("GM2 Gangliozid", True, "Heksozaminidaz A eksikliğinde biriken lipid")]
            ]
        ),
        14: make_table(
            ["Etiyoloji", "Hücresel Bozukluk Basamağı", "Tipik Morfoloji"],
            [
                [("Alkol Toksisitesi", False, ""), ("NADH artışı ile beta-oksidasyon blokajı", True, "Mitokondriyal yağ yakımının durması"), ("Makroveziküler steatoz", False, "")],
                [("Obezite ve Tip 2 Diyabet", False, ""), ("İnsülin direnciyle aşırı serbest yağ asidi girişi", True, "Kontrolsüz adipoz lipoliz akışı"), ("Makroveziküler steatoz", False, "")],
                [("Kvaşiorkor (Malnütrisyon)", False, ""), ("Apolipoprotein sentez yetersizliği", True, "Lipoprotein paketleme defekti"), ("Hepatomegali ve yağlanma", False, "")],
                [("Reye Sendromu", False, ""), ("Mitokondriyal mikrovakuoler lipid birikimi", True, "Akut mitokondri hasarı"), ("Mikroveziküler steatoz", False, "")]
            ]
        ),
        24: make_table(
            ["Ateroskleroz Evresi", "Baskın Hücresel / Dokusal Yapı", "Klinik Özellik"],
            [
                [("Yağlı Çizgilenme (Fatty Streak)", False, ""), ("İntimada toplanmış köpük hücreler", True, "Kolesterol yüklü makrofaj kümeleri"), ("Asemptomatik, erken çocuklukta başlar", False, "")],
                [("Aterom Plağı", False, ""), ("Nekrotik lipid çekirdek ve fibröz şapka", True, "Kolesterol kristalleri ve düz kas hücreleri"), ("Lümeni daraltır, anjina yapabilir", False, "")],
                [("Komplike Plak", False, ""), ("Rüptür, kalsifikasyon ve trombüs", True, "Damar duvarının yırtılması"), ("Akut miyokard enfarktüsü ve inme", False, "")]
            ]
        ),
        34: make_table(
            ["İnklüzyon Adı", "Hücre Tipi", "Organel Lokalizasyonu", "Biriken Madde"],
            [
                [("Russell Cisimciği", False, ""), ("Plazma hücresi", False, ""), ("Granüllü ER sisternaları", True, "Genişlemiş GER lümeni"), ("İmmünoglobulin küreleri", False, "")],
                [("Dutcher Cisimciği", False, ""), ("Malign plazma hücresi", False, ""), ("Nükleus psödoinklüzyonu", True, "Çekirdeğe invajinasyon"), ("İmmünoglobulin", False, "")],
                [("Mallory-Denk", False, ""), ("Hepatosit", False, ""), ("Serbest sitoplazma (perinükleer)", True, "Çekirdek komşuluğunda kordlar"), ("Sitokeratin 8/18 ve ubikitin", False, "")]
            ]
        ),
        44: make_table(
            ["Hastalık", "Mutant Protein", "Hücresel Mekanizma", "Klinik Sonuç"],
            [
                [("Kistik Fibrozis", False, ""), ("CFTR", False, ""), ("ER'de erken proteazomal yıkım", True, "Zara çıkamayan klor kanalı"), ("Koyu sekresyon, bronşiektazi", False, "")],
                [("Ailesel Hiperkolesterolemi", False, ""), ("LDL Reseptörü", False, ""), ("ER'den Golgi'ye taşınamama", True, "Hücre yüzeyinde reseptör yokluğu"), ("Erken ateroskleroz, ksantom", False, "")],
                [("Creutzfeldt-Jakob", False, ""), ("Prion (PrPSc)", False, ""), ("Beta kırmalı bükülme ve agregasyon", True, "Nörotoksik çözünmeyen agregat"), ("Hızlı ölümcül demans", False, "")]
            ]
        ),
        54: make_table(
            ["Klinik Durum", "Tutulan Organ ve Doku", "Mikroskobik Görünüm", "PAS Reaksiyonu"],
            [
                [("Diyabet (Armanni-Ebstein)", False, ""), ("Böbrek proksimal tübülü", False, ""), ("Berrak vakuollü epitel", True, "Glikojen dolu tübül hücreleri"), ("PAS pozitif, diyastaz duyarlı", False, "")],
                [("Diyabetik Karaciğer", False, ""), ("Hepatosit nükleusu", False, ""), ("Glikojenli nükleus", True, "Çekirdekte vakuolizasyon"), ("PAS pozitif, diyastaz duyarlı", False, "")],
                [("Von Gierke Hastalığı", False, ""), ("Karaciğer ve böbrekler", False, ""), ("Masif parankimal glikojen", True, "G6Paz eksikliğinde göllenme"), ("PAS pozitif, diyastaz duyarlı", False, "")]
            ]
        ),
        64: make_table(
            ["Pigment", "Kökeni", "Işık Mikroskopisi Rengi", "Özel Boyanma Özelliği"],
            [
                [("Karbon (Antrakozis)", False, ""), ("Eksojen hava kirliliği", False, ""), ("Siyah partiküller", True, "Alveoler makrofajda siyah taneler"), ("Özel boya gerekmez, inerttir", False, "")],
                [("Lipofusin", False, ""), ("Endojen lipid peroksidasyonu", False, ""), ("Altın sarısı-kahverengi", True, "Perinükleer ince granüller"), ("Prusya mavisi negatiftir", False, "")],
                [("Melanin", False, ""), ("Endojen melanosit sentezi", False, ""), ("Kahverengi-siyah", True, "Keratinosit çekirdeği üstü"), ("Fontana-Masson ile pozitif siyah", False, "")]
            ]
        ),
        74: make_table(
            ["Hemosideroz Tipi", "Etiyoloji", "Demirin Biriktiği Hücreler", "Doku Hasarı / Fibrozis"],
            [
                [("Lokal Hemosideroz", False, ""), ("Hematom, ekimoz, konjesyon", False, ""), ("Doku makrofajları (siderofaj)", True, "Eritrosit yutan histiositler"), ("Yok (lokal rezorpsiyon)", False, "")],
                [("Sistemik Hemosideroz", False, ""), ("Transfüzyon, kronik hemoliz", False, ""), ("Kupffer, dalak ve kemik iliği", True, "RES makrofaj ağı"), ("Erken evrede yok", False, "")],
                [("Hemokromatoz", False, ""), ("HFE mutasyonu (primer)", False, ""), ("Hepatosit, pankreas, miyosit", True, "Parankimal hücreler"), ("Var (Siroz, diyabet, kalp yetmezliği)", False, "")]
            ]
        ),
        84: make_table(
            ["Kalsifikasyon Fazı", "Lokalizasyon", "Anahtar Moleküler Mekanizma", "Kristal Tipi"],
            [
                [("İntraselüler Çekirdeklenme", False, ""), ("Nekrotik mitokondri", True, "Organel iç matriksi"), ("Aşırı Ca2+ ve PO4 presipitasyonu", False, ""), ("Hidroksiapatit nükleusu", False, "")],
                [("Ekstraselüler Çekirdeklenme", False, ""), ("Membran matriks vezikülleri", True, "Zardan kopan parçacıklar"), ("Fosfatidilserin ve alkalen fosfataz", False, ""), ("Hidroksiapatit kristalleri", False, "")],
                [("Kristal Yayılması (Propagasyon)", False, ""), ("Kollajen ve interstisyel matriks", True, "Hücreler arası bağ doku"), ("Kristallerin birleşip büyümesi", False, ""), ("Makroskopik tebeşirsi kalsifikasyon", False, "")]
            ]
        ),
        94: make_table(
            ["Etiyolojik Grup", "Hastalık Örneği", "Hiperkalsemi Mekanizması", "Baskın Kalsifikasyon Alanı"],
            [
                [("PTH Fazlalığı", False, ""), ("Primer Hiperparatiroidizm", False, ""), ("Paratiroid adenomu ile kemik rezorpsiyonu", True, "Aşırı osteoklastik kemik erimesi"), ("Mide, böbrek, akciğer", False, "")],
                [("KBY ve Fosfat Yükü", False, ""), ("Sekonder Hiperparatiroidizm", False, ""), ("Fosfat retansiyonu ve yüksek Ca × P", True, "Böbrekten fosfat atılamaması"), ("Küçük damarlar (kalsifilaksi)", False, "")],
                [("Kemik Yıkımı", False, ""), ("Multipl Miyelom", False, ""), ("Litik punched-out kemik erimesi", True, "Sitokin aracılı osteoliz"), ("Böbrek tübülleri (nefrokalsinoz)", False, "")],
                [("D Vitamini Aktivasyonu", False, ""), ("Sarkoidoz Granülomları", False, ""), ("Makrofajlarda 1α-hidroksilaz ekspresyonu", True, "PTH'dan bağımsız kalsitriyol üretimi"), ("Alveol septaları ve mide", False, "")]
            ]
        )
    }

def main():
    print("=" * 70)
    print("Kurul 1 - Ders 7: Hücre İçi Birikimler ve Kalsifikasyonlar")
    print("Multi-Format İnteraktif Öğrenme Destesi Oluşturuluyor...")
    print("=" * 70)

    # 1. TÜM BÖLÜM SLAYTLARINI TOPLA
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
            q_id = q.get("id") or f"k1-07-q{len(questions)+1:02d}"
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
    extra_quizzes = build_extra_micro_quizzes()
    extra_causal = build_extra_causal_chains()
    extra_sliders = build_extra_before_after_sliders()
    extra_branching = build_extra_branching_logic()
    extra_tables = build_extra_tables()

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
            if not slide.get("flashcards"):
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

        # Şema normalizasyonları ve sızıntı temizliği
        for el in elements:
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
    deck_id = "k1p-k1-07-hucre-ici-birikimler-ve-kalsifikasyonlar"
    deck_title = "Hücre İçi Birikimler ve Kalsifikasyonlar (Yeni Mikro-Ders)"
    short_title = "Hücre İçi Birikimler ve Kalsifikasyonlar"

    os.makedirs(PACKAGE_DIR, exist_ok=True)
    os.makedirs(DECKS_ITEMS_DIR, exist_ok=True)

    # Manifest
    manifest_data = {
        "id": "k1-07-hucre-ici-birikimler-ve-kalsifikasyonlar",
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
        "audioFile": "audio/decks/k1-07.mp3",
        "audioDuration": 2400,
        "confidence": 0.99,
        "themeColor": "amber",
        "matchedNoteId": "k1-07",
        "matchedNoteTitle": "Hücre İçi Birikimler ve Kalsifikasyonlar",
        "isNew": True,
        "isLegacy": False,
        "version": "2.0.0",
        "packageSources": {
            "packageDir": "meds/src/data/decks/packages/k1-07-hucre-ici-birikimler-ve-kalsifikasyonlar",
            "manifest": "manifest.json",
            "structure": "structure.xml",
            "blocks": "blocks.html",
            "content": "content.md"
        },
        "overview": (
            "Hücre içi ve dışı anormal birikimlerin 4 temel mekanizması; trigliserid, kolesterol, "
            "protein, glikojen ve pigment depolanmaları; distrofik ve metastatik kalsifikasyon patogenezi."
        ),
        "highYieldPearls": [
            "Hücre içi birikim mekanizmaları: yetersiz klirens, mutant protein, eksojen partikül, lizozomal defekt.",
            "Steatoz parankimde trigliserid birikimidir; alkolde artan NADH beta-oksidasyonu bloke eder.",
            "Aterosklerozda köpük hücreler oxLDL'yi çöpçü reseptörlerle geri bildirimsiz yutar.",
            "Aşil tendonu ksantomu ailesel hiperkolesterolemi için patognomoniktir.",
            "Russell cisimciği plazma hücresi GER'inde immünoglobulin birikimidir.",
            "Mallory-Denk cisimcikleri sitokeratin 8/18 ara filamentleri ve ubikitinden oluşur.",
            "α1-Antitripsin eksikliği hepatosit ER'sinde PAS(+) granül ve siroz, akciğerde amfizem yapar.",
            "Glikojen PAS pozitif ve diyastaz duyarlıdır; diyabette Armanni-Ebstein tübülleri görülür.",
            "Pompe lizozomal asit maltaz eksikliğidir; normoglisemi ve masif kardiyomegali yapar.",
            "Lipofusin aşınma pigmentidir (lipid peroksidasyonu); yaşlı kalpte kahverengi atrofi yapar.",
            "Hemosiderin Prusya mavisiyle boyanır; sol kalp yetmezliğinde kalp hata hücreleri oluşur.",
            "Distrofik kalsifikasyonda serum Ca normaldir, nekrotik dokularda mitokondride başlar.",
            "Metastatik kalsifikasyon hiperkalsemi ile normal dokularda (mide, böbrek, akciğer) alkaloz nedeniyle çöker."
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
        if d.get("id") == deck_id or d.get("id") == "k1-07-hucre-ici-birikimler-ve-kalsifikasyonlar":
            found_idx = i
            break

    deck_summary = {
        "id": deck_id,
        "title": deck_title,
        "shortTitle": short_title,
        "discipline": "Tıbbi Patoloji",
        "committee": "Kurul 1 (Ürogenital ve Solunum Sistemi)",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "audioFile": "audio/decks/k1-07.mp3",
        "audioDuration": 2400,
        "confidence": 0.99,
        "themeColor": "amber",
        "matchedNoteId": "k1-07",
        "matchedNoteTitle": "Hücre İçi Birikimler ve Kalsifikasyonlar",
        "isNew": True,
        "isLegacy": False,
        "version": "2.0.0",
        "packageSources": {
            "packageDir": "meds/src/data/decks/packages/k1-07-hucre-ici-birikimler-ve-kalsifikasyonlar",
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
    print("TEBRİKLER! DERS 7 TÜM FORMATLARDA BAŞARIYLA TAMAMLANDI!")
    print("=" * 70)

if __name__ == "__main__":
    main()
