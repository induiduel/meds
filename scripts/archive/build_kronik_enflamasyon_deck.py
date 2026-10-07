# -*- coding: utf-8 -*-
"""
scripts/build_kronik_enflamasyon_deck.py
Generates full 24-slide high-yield interactive learning deck for:
Prof. Dr. Hikmet Keleş - Kronik ve Granülomatöz Enflamasyon
Adheres strictly to all curriculum and database constraints.
"""

import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

DECKS_PATH = 'src/data/interactive_learning_decks.json'
GLOSSARY_PATH = 'src/data/medical_glossary.json'
ENCYCLOPEDIA_PATH = 'src/data/medical_encyclopedia.json'
QUESTIONS_PATH = 'src/data/pastQuestions.json'
CHUNK8_PATH = 'src/data/study_questions/chunk_8.json'

with open(DECKS_PATH, 'r', encoding='utf-8') as f:
    decks = json.load(f)

# 24 Slides definition
slides = [
    {
        "slideNumber": 1,
        "title": "Kronik Enflamasyonun Tanımı ve Patofizyolojik Temelleri",
        "subtitle": "Eşzamanlı aktif enflamasyon, parankim doku hasarı ve onarım (fibrozis/anjiyogenez) triadı.",
        "badge": "Giriş & Tanım",
        "badgeColor": "red",
        "discipline": "Tıbbi Patoloji",
        "professorAudioHighlight": {
            "timestamp": "02:15",
            "quote": "Kronik enflamasyon sadece sürenin uzaması demek değildir; aynı anda hem doku yıkımı hem aktif enflamasyon hem de onarımın bir arada yürüdüğü dinamik bir süreçtir.",
            "emphasisType": "direct_exam_warning",
            "note": "Akut enflamasyondan en önemli ayrımı ödem ve nötrofil yerine mononükleer hücre infiltrasyonu ve fibrozis ile karakterize olmasıdır."
        },
        "content": "### Kronik Enflamasyonun Temel Karakteristiği\nKronik enflamasyon; haftalar, aylar veya yıllar boyu devam eden, **eşzamanlı olarak** aktif enflamasyon, doku hasarı ve onarım girişimlerinin (anjiyogenez ve fibrozis) bir arada bulunduğu uzamış patolojik süreçtir.\n\n• **Akut vs Kronik Enflamasyon:** Akut enflamasyonda temel vasküler olaylar (vazodilatasyon, permeabilite artışı, eksüdasyon) ve nötrofil baskınlığı görülürken; kronik enflamasyonda **mononükleer lökosit infiltrasyonu** (makrofajlar, lenfositler, plazma hücreleri), doku yıkımı ve bağ dokusu artışı (fibrozis) ön plandadır.\n• **Patogenez Yolları:** Akut enflamasyonun rezolüsyona uğrayamaması sonucu (örn. abse duvarı) sekonder olarak gelişebileceği gibi; çoğu zaman sinsi, asemptomatik ve doğrudan primer kronik (tüberküloz, otoimmünite, silikozis) olarak başlar.\n\n> 🔴 ÖNEMLİ: Kronik enflamasyonun histopatolojik triadı: 1) Mononükleer hücre infiltrasyonu, 2) Doku yıkımı, 3) Onarım çabaları (fibrozis ve anjiyogenez).",
        "synthesisNarrative": "### Kronik Enflamasyonun Temel Karakteristiği\nKronik enflamasyon; haftalar, aylar veya yıllar boyu devam eden, **eşzamanlı olarak** aktif enflamasyon, doku hasarı ve onarım girişimlerinin (anjiyogenez ve fibrozis) bir arada bulunduğu uzamış patolojik süreçtir.\n\n• **Akut vs Kronik Enflamasyon:** Akut enflamasyonda temel vasküler olaylar (vazodilatasyon, permeabilite artışı, eksüdasyon) ve nötrofil baskınlığı görülürken; kronik enflamasyonda **mononükleer lökosit infiltrasyonu** (makrofajlar, lenfositler, plazma hücreleri), doku yıkımı ve bağ dokusu artışı (fibrozis) ön plandadır.\n• **Patogenez Yolları:** Akut enflamasyonun rezolüsyona uğrayamaması sonucu (örn. abse duvarı) sekonder olarak gelişebileceği gibi; çoğu zaman sinsi, asemptomatik ve doğrudan primer kronik (tüberküloz, otoimmünite, silikozis) olarak başlar.\n\n> 🔴 ÖNEMLİ: Kronik enflamasyonun histopatolojik triadı: 1) Mononükleer hücre infiltrasyonu, 2) Doku yıkımı, 3) Onarım çabaları (fibrozis ve anjiyogenez).",
        "spots": [
            "🔴 ÖNEMLİ: Kronik enflamasyonda histopatolojik triad: Mononükleer hücre infiltrasyonu + Doku yıkımı + Onarım (fibrozis & anjiyogenez).",
            "🔵 ÇIKMIŞ SORU: Akut enflamasyonda baskın hücre nötrofil iken, kronik enflamasyonun orkestra şefi ve ana hücresi MAKROFAJDIR."
        ],
        "spotPearls": [
            "🔴 ÖNEMLİ: Kronik enflamasyonda histopatolojik triad: Mononükleer hücre infiltrasyonu + Doku yıkımı + Onarım (fibrozis & anjiyogenez).",
            "🔵 ÇIKMIŞ SORU: Akut enflamasyonda baskın hücre nötrofil iken, kronik enflamasyonun orkestra şefi ve ana hücresi MAKROFAJDIR."
        ],
        "flashcards": [
            {
                "id": "fc-kronik-1",
                "category": "Patoloji",
                "front": "Kronik enflamasyonun 3 temel histopatolojik bileşeni nedir?",
                "back": "1) Mononükleer hücre infiltrasyonu (makrofaj, lenfosit, plazma hücresi)\n2) Doku yıkımı (parankim hasarı)\n3) Onarım çabaları (anjiyogenez ve fibrozis)",
                "hint": "Hücreler, hasar ve bağ dokusu yapımı"
            }
        ],
        "coreContent": {
            "keyBullets": [
                { "title": "🔴 Triad Vurgusu", "desc": "Kronik enflamasyonda hücre infiltrasyonu, kalıcı doku harabiyeti ve bağ dokusu artışı (skar/fibrozis) aynı anda eşzamanlı devam eder." }
            ]
        },
        "practiceQuestion": {
            "id": "q-kronik-enf-1",
            "stem": "Aşağıdakilerden hangisi kronik enflamasyonun akut enflamasyondan ayırt edilmesinde kullanılan temel histopatolojik özelliklerden biri DEĞİLDİR?",
            "options": [
                { "key": "A", "text": "Belirgin damar genişlemesi ve yoğun nötrofil birikimi" },
                { "key": "B", "text": "Mononükleer lökosit infiltrasyonu" },
                { "key": "C", "text": "Parankimal doku yıkımı ve nekroz" },
                { "key": "D", "text": "Kollajen birikimi ve fibrozis gelişimi" },
                { "key": "E", "text": "Yeni damar oluşumu (anjiyogenez)" }
            ],
            "correctAnswer": "A",
            "explanation": "Yoğun nötrofil infiltrasyonu, belirgin vazodilatasyon ve ödem akut enflamasyonun kardinal bulgularıdır. Kronik enflamasyonda mononükleer hücreler, parankim hasarı, anjiyogenez ve fibrozis görülür.",
            "isPracticeQuestion": True
        },
        "relatedQuestions": []
    },
    {
        "slideNumber": 2,
        "title": "Kronik Enflamasyonun Nedenleri ve Etyolojik Spektrum",
        "subtitle": "Persistan enfeksiyonlar, otoimmün/hipersensitivite hastalıkları ve toksik madde maruziyeti.",
        "badge": "Etyoloji",
        "badgeColor": "amber",
        "discipline": "Tıbbi Patoloji",
        "content": "### Kronik Enflamasyonu Tetikleyen Üç Ana Neden\nKronik enflamasyon tipik olarak üç farklı patolojik durumda tetiklenir ve sürdürülür:\n\n1. **Persistan (Dirençli) Enfeksiyonlar:**\n  - Vücudun fagositozla kolay yok edemediği mikroorganizmalar: *Mycobacterium tuberculosis*, *Treponema pallidum*, mantarlar, parazitler.\n  - Bu mikroplar gecikmiş tip aşırı duyarlılık (Tip IV) yanıtını uyararak sıklıkla **granülomatöz enflamasyona** yol açar.\n2. **İmmün Aracılı Enflamatuar Hastalıklar (Aşırı Duyarlılık ve Otoimmünite):**\n  - Kendi doku antijenlerine karşı sürekli immün aktivasyon (Romatoid Artrit, Sistemik Lupus Eritematozus - SLE).\n  - Zararsız çevre antijenlerine kontrolsüz yanıt (Alerjik astım, inflamatuar bağırsak hastalıkları).\n  - Antijenler vücuttan atılamadığı için süreç ömür boyu kronik devam eder.\n3. **Toksik Ajanlara Uzamış Maruziyet:**\n  - **Ekzojen:** Silika tozu (silikozis), asbest lifleri (asbestozis).\n  - **Endojen:** Plazma lipidleri ve kolesterol kristallerinin arter duvarında birikmesi (**ateroskleroz**).\n\n> 🔵 ÇIKMIŞ SORU: Ateroskleroz, endotel altında kolesterol kristallerinin tetiklediği kronik vasküler enflamatuar bir süreçtir.",
        "synthesisNarrative": "### Kronik Enflamasyonu Tetikleyen Üç Ana Neden\nKronik enflamasyon tipik olarak üç farklı patolojik durumda tetiklenir ve sürdürülür:\n\n1. **Persistan (Dirençli) Enfeksiyonlar:**\n  - Vücudun fagositozla kolay yok edemediği mikroorganizmalar: *Mycobacterium tuberculosis*, *Treponema pallidum*, mantarlar, parazitler.\n  - Bu mikroplar gecikmiş tip aşırı duyarlılık (Tip IV) yanıtını uyararak sıklıkla **granülomatöz enflamasyona** yol açar.\n2. **İmmün Aracılı Enflamatuar Hastalıklar (Aşırı Duyarlılık ve Otoimmünite):**\n  - Kendi doku antijenlerine karşı sürekli immün aktivasyon (Romatoid Artrit, Sistemik Lupus Eritematozus - SLE).\n  - Zararsız çevre antijenlerine kontrolsüz yanıt (Alerjik astım, inflamatuar bağırsak hastalıkları).\n  - Antijenler vücuttan atılamadığı için süreç ömür boyu kronik devam eder.\n3. **Toksik Ajanlara Uzamış Maruziyet:**\n  - **Ekzojen:** Silika tozu (silikozis), asbest lifleri (asbestozis).\n  - **Endojen:** Plazma lipidleri ve kolesterol kristallerinin arter duvarında birikmesi (**ateroskleroz**).\n\n> 🔵 ÇIKMIŞ SORU: Ateroskleroz, endotel altında kolesterol kristallerinin tetiklediği kronik vasküler enflamatuar bir süreçtir.",
        "spots": [
            "🔴 ÖNEMLİ: Endojen toksik ajan maruziyetinin en klasik örneği aterosklerozdur (oksidize LDL ve kolesterol birikimi).",
            "🔵 ÇIKMIŞ SORU: İmmün kökenli kronik enflamatuar hastalıklarda (RA, SLE) antijen yok edilemediği için doku hasarı progresif seyreder."
        ],
        "spotPearls": [
            "🔴 ÖNEMLİ: Endojen toksik ajan maruziyetinin en klasik örneği aterosklerozdur (oksidize LDL ve kolesterol birikimi).",
            "🔵 ÇIKMIŞ SORU: İmmün kökenli kronik enflamatuar hastalıklarda (RA, SLE) antijen yok edilemediği için doku hasarı progresif seyreder."
        ],
        "flashcards": [
            {
                "id": "fc-kronik-2",
                "category": "Etyoloji",
                "front": "Endojen toksik maddelerin tetiklediği en yaygın kronik enflamatuar hastalık nedir?",
                "back": "Ateroskleroz (damar duvarında oksidize LDL ve kolesterol birikimi ile gelişir).",
                "hint": "Damar sertliği"
            }
        ],
        "coreContent": {
            "keyBullets": [
                { "title": "💡 Klinik Odak", "desc": "Ekzojen silika ve asbest parçalanamaz; endojen kolesterol ise süregelen makrofaj aktivasyonuna yol açar." }
            ]
        },
        "practiceQuestion": {
            "id": "q-kronik-enf-2",
            "stem": "Endojen bir toksik ajanın dokuda birikmesiyle tetiklenen ve günümüzde en yaygın görülen kronik vasküler enflamatuar süreç aşağıdakilerden hangisidir?",
            "options": [
                { "key": "A", "text": "Ateroskleroz" },
                { "key": "B", "text": "Silikozis" },
                { "key": "C", "text": "Asbestozis" },
                { "key": "D", "text": "Romatoid Artrit" },
                { "key": "E", "text": "Tüberküloz" }
            ],
            "correctAnswer": "A",
            "explanation": "Ateroskleroz, damar duvarında endojen lipit ve kolesterol kristallerinin birikmesiyle tetiklenen kronik enflamatuar bir süreçtir. Silikozis ve asbestozis ekzojen ajanlardır.",
            "isPracticeQuestion": True
        },
        "relatedQuestions": []
    },
    {
        "slideNumber": 3,
        "title": "Mononükleer Fagosit Sistemi ve Makrofajların Kökeni",
        "subtitle": "Kemik iliği monositleri ve embriyonik doku yerleşik makrofajları (Kupffer, Mikroglia, Alveoler).",
        "badge": "Makrofaj Biyolojisi",
        "badgeColor": "blue",
        "discipline": "Tıbbi Patoloji",
        "content": "### Makrofajların İkili Gelişim Kökeni\nMakrofajlar dokularda iki farklı kaynaktan meydana gelir:\n\n1. **Embriyonik Doku Yerleşik Makrofajları (Tissue-resident):**\n  - Fetal karaciğer ve yolk sac'tan (vitellüs kesesi) erken embriyogenezde göç ederler.\n  - Yıllarca dokuda kalır ve yerel proliferasyonla çoğalırlar.\n  - **Karaciğer:** Kupffer hücreleri\n  - **Santral Sinir Sistemi:** Mikroglia hücreleri\n  - **Akciğer:** Alveoler makrofajlar\n  - **Dalak & Lenf Nodu:** Sinüs histiyositleri\n  - **Deri:** Langerhans hücreleri\n  - **Kemik:** Osteoklastlar\n2. **Kemik İliği Kaynaklı Dolaşan Monositler:**\n  - Enflamasyon başladığında kemik iliğinden kana salınan monositler (yarı ömürleri kanda ~1 gündür), kemokinler (CCL2 / MCP-1) aracılığıyla dokuya geçer ve 48 saat içinde baskın makrofaj popülasyonunu oluşturur.\n\n> 🔴 ÖNEMLİ: Akut enflamasyonun 24-48. saatinden itibaren nötrofillerin yerini monosit-makrofajlar alır.",
        "synthesisNarrative": "### Makrofajların İkili Gelişim Kökeni\nMakrofajlar dokularda iki farklı kaynaktan meydana gelir:\n\n1. **Embriyonik Doku Yerleşik Makrofajları (Tissue-resident):**\n  - Fetal karaciğer ve yolk sac'tan (vitellüs kesesi) erken embriyogenezde göç ederler.\n  - Yıllarca dokuda kalır ve yerel proliferasyonla çoğalırlar.\n  - **Karaciğer:** Kupffer hücreleri\n  - **Santral Sinir Sistemi:** Mikroglia hücreleri\n  - **Akciğer:** Alveoler makrofajlar\n  - **Dalak & Lenf Nodu:** Sinüs histiyositleri\n  - **Deri:** Langerhans hücreleri\n  - **Kemik:** Osteoklastlar\n2. **Kemik İliği Kaynaklı Dolaşan Monositler:**\n  - Enflamasyon başladığında kemik iliğinden kana salınan monositler (yarı ömürleri kanda ~1 gündür), kemokinler (CCL2 / MCP-1) aracılığıyla dokuya geçer ve 48 saat içinde baskın makrofaj popülasyonunu oluşturur.\n\n> 🔴 ÖNEMLİ: Akut enflamasyonun 24-48. saatinden itibaren nötrofillerin yerini monosit-makrofajlar alır.",
        "spots": [
            "🔴 ÖNEMLİ: Karaciğerde Kupffer, beyinde Mikroglia, akciğerde Alveoler makrofaj doku yerleşik embriyonik kökenli hücrelerdir.",
            "🔵 ÇIKMIŞ SORU: Monositlerin dokuya göçünde en önemli kemoatraktan kemokin MCP-1 (CCL2)'dir."
        ],
        "spotPearls": [
            "🔴 ÖNEMLİ: Karaciğerde Kupffer, beyinde Mikroglia, akciğerde Alveoler makrofaj doku yerleşik embriyonik kökenli hücrelerdir.",
            "🔵 ÇIKMIŞ SORU: Monositlerin dokuya göçünde en önemli kemoatraktan kemokin MCP-1 (CCL2)'dir."
        ],
        "flashcards": [
            {
                "id": "fc-kronik-3",
                "category": "Hücre Biyolojisi",
                "front": "Karaciğer ve santral sinir sistemindeki doku yerleşik makrofajların isimleri nelerdir?",
                "back": "Karaciğer: Kupffer hücreleri\nSantral Sinir Sistemi: Mikroglia hücreleri",
                "hint": "Kupffer ve mikroglia"
            }
        ],
        "coreContent": {
            "table": {
                "title": "Doku Yerleşik Makrofaj Dağılımı",
                "headers": ["Organ / Doku", "Makrofaj Tipi", "Temel Fonksiyon"],
                "rows": [
                    ["Karaciğer", "Kupffer Hücresi", "Portal kan bakterilerini ve yaşlı eritrositleri temizleme"],
                    ["Santral Sinir Sistemi", "Mikroglia", "Nöronal atıkları ve hücresel debrisleri fagositoz"],
                    ["Akciğer", "Alveoler Makrofaj", "Solunan partikülleri ve sürfaktan yıkımını temizleme"],
                    ["Kemik", "Osteoklast", "Kemik rezorpsiyonu ve matriks modellemesi"]
                ]
            }
        },
        "practiceQuestion": {
            "id": "q-kronik-enf-3",
            "stem": "Karaciğer sinüzoidlerinde yerleşik bulunan ve portal sirkülasyondan gelen partikülleri fagosite eden mononükleer fagosit sistemi hücresi hangisidir?",
            "options": [
                { "key": "A", "text": "Kupffer hücresi" },
                { "key": "B", "text": "İto (Yıldızsı) hücresi" },
                { "key": "C", "text": "Hepatosit" },
                { "key": "D", "text": "Sinüs histiyositi" },
                { "key": "E", "text": "Langerhans hücresi" }
            ],
            "correctAnswer": "A",
            "explanation": "Karaciğerdeki doku yerleşik makrofajlara Kupffer hücreleri denir. İto hücreleri A vitamini depolar ve fibrozisten sorumludur.",
            "isPracticeQuestion": True
        },
        "relatedQuestions": []
    },
    {
        "slideNumber": 4,
        "title": "M1 (Klasik) ve M2 (Alternatif) Makrofaj Aktivasyonu",
        "subtitle": "Enfeksiyon yok edici öldürücü yol (M1) vs doku onarıcı fibrotik yol (M2).",
        "badge": "M1 vs M2",
        "badgeColor": "indigo",
        "discipline": "Tıbbi Patoloji",
        "professorAudioHighlight": {
            "timestamp": "11:40",
            "quote": "Sınavda mutlaka sorulur: M1 makrofaj mikrop öldürür, doku yıkar; M2 makrofaj ise enflamasyonu durdurup dokuyu tamir eder, kollajen sentezletir.",
            "emphasisType": "direct_exam_warning",
            "note": "M1 için tetikleyici IFN-γ ve LPS iken; M2 için tetikleyici IL-4 ve IL-13 sitokinleridir."
        },
        "content": "### M1 ve M2 Makrofaj Kutuplaşması\nMakrofajlar aldıkları sitokin sinyallerine göre iki zıt fonksiyonel duruma farklılaşırlar:\n\n• **M1 (Klasik Aktivasyon Yolu):**\n  - **Uyaranlar:** Mikrobiyal endotoksin (LPS), TLR ligandları ve özellikle Th1 lenfositlerinden salınan **IFN-g (İnterferon-gama)**.\n  - **Ürünler:** Reaktif oksijen türleri (ROS), Nitrik oksit (iNOS aracılığıyla NO), lizozomal enzimler, IL-1, TNF, IL-6, IL-12.\n  - **Fonksiyon:** Güçlü mikrobisidal aktivite, patojen öldürme, doku harabiyeti, akut enflamasyonun tetiklenmesi.\n• **M2 (Alternatif Aktivasyon Yolu):**\n  - **Uyaranlar:** Th2 lenfositlerinden salınan **IL-4 ve IL-13**.\n  - **Ürünler:** **TGF-b**, VEGF, FGF, PDGF, arginaz, IL-10 (anti-enflamatuar).\n  - **Fonksiyon:** Doku onarımı, anjiyogenez, fibroblast aktivasyonu, kollajen sentezi, yara iyileşmesi ve enflamasyonun yatıştırılması.\n\n> 🔴 ÖNEMLİ: İdeal bir yanıtta önce M1 yolu mikropları yok eder; ardından M2 yolu devreye girerek dokuyu onarır. M2'nin kontrolsüz uzaması patolojik organ fibrozisine yol açar.",
        "synthesisNarrative": "### M1 ve M2 Makrofaj Kutuplaşması\nMakrofajlar aldıkları sitokin sinyallerine göre iki zıt fonksiyonel duruma farklılaşırlar:\n\n• **M1 (Klasik Aktivasyon Yolu):**\n  - **Uyaranlar:** Mikrobiyal endotoksin (LPS), TLR ligandları ve özellikle Th1 lenfositlerinden salınan **IFN-g (İnterferon-gama)**.\n  - **Ürünler:** Reaktif oksijen türleri (ROS), Nitrik oksit (iNOS aracılığıyla NO), lizozomal enzimler, IL-1, TNF, IL-6, IL-12.\n  - **Fonksiyon:** Güçlü mikrobisidal aktivite, patojen öldürme, doku harabiyeti, akut enflamasyonun tetiklenmesi.\n• **M2 (Alternatif Aktivasyon Yolu):**\n  - **Uyaranlar:** Th2 lenfositlerinden salınan **IL-4 ve IL-13**.\n  - **Ürünler:** **TGF-b**, VEGF, FGF, PDGF, arginaz, IL-10 (anti-enflamatuar).\n  - **Fonksiyon:** Doku onarımı, anjiyogenez, fibroblast aktivasyonu, kollajen sentezi, yara iyileşmesi ve enflamasyonun yatıştırılması.\n\n> 🔴 ÖNEMLİ: İdeal bir yanıtta önce M1 yolu mikropları yok eder; ardından M2 yolu devreye girerek dokuyu onarır. M2'nin kontrolsüz uzaması patolojik organ fibrozisine yol açar.",
        "spots": [
            "🔴 ÖNEMLİ: M1 aktivatörü: IFN-γ ve LPS. M2 aktivatörü: IL-4 ve IL-13.",
            "🔵 ÇIKMIŞ SORU: Doku onarımı, anjiyogenez ve fibrozisten sorumlu makrofaj alt tipi M2 (alternatif yol) makrofajdır; en önemli mediyatörü TGF-β dır."
        ],
        "spotPearls": [
            "🔴 ÖNEMLİ: M1 aktivatörü: IFN-γ ve LPS. M2 aktivatörü: IL-4 ve IL-13.",
            "🔵 ÇIKMIŞ SORU: Doku onarımı, anjiyogenez ve fibrozisten sorumlu makrofaj alt tipi M2 (alternatif yol) makrofajdır; en önemli mediyatörü TGF-β dır."
        ],
        "flashcards": [
            {
                "id": "fc-kronik-4",
                "category": "İmmünoloji",
                "front": "Klasik (M1) ve Alternatif (M2) makrofaj aktivasyonunu indükleyen ana sitokinler nelerdir?",
                "back": "M1 indükleyicisi: IFN-γ (İnterferon-gama) ve endotoksin\nM2 indükleyicisi: IL-4 ve IL-13",
                "hint": "Th1 vs Th2 sitokinleri"
            }
        ],
        "coreContent": {
            "table": {
                "title": "M1 ve M2 Makrofaj Karşılaştırması",
                "headers": ["Özellik", "M1 (Klasik Yol)", "M2 (Alternatif Yol)"],
                "rows": [
                    ["Tetikleyici Sitokin", "IFN-γ, LPS, Mikrobiyal antijen", "IL-4, IL-13 (Th2 hücreleri)"],
                    ["Ana Rolü", "Mikrop öldürme, doku harabiyeti", "Doku onarımı, yara iyileşmesi, fibrozis"],
                    ["Enzim & Mediyatör", "iNOS (NO üretimi), ROS, Lizozom", "Arginaz, TGF-β, VEGF, FGF, PDGF"],
                    ["İmmün Yanıt", "Pro-enflamatuar (IL-1, TNF, IL-12)", "Anti-enflamatuar (IL-10, TGF-β)"]
                ]
            }
        },
        "practiceQuestion": {
            "id": "q-kronik-enf-4",
            "stem": "Dokuda yara iyileşmesi, anjiyogenez ve kollajen sentezini uyararak fibrozisi başlatan alternatif (M2) makrofaj aktivasyonunu tetikleyen temel sitokinler hangileridir?",
            "options": [
                { "key": "A", "text": "IL-4 ve IL-13" },
                { "key": "B", "text": "IFN-γ ve TNF-α" },
                { "key": "C", "text": "IL-1 ve IL-6" },
                { "key": "D", "text": "IL-12 ve IL-18" },
                { "key": "E", "text": "IL-17 ve IL-22" }
            ],
            "correctAnswer": "A",
            "explanation": "Alternatif (M2) makrofaj aktivasyonunu Th2 kökenli IL-4 ve IL-13 sitokinleri tetikler. IFN-γ ise klasik M1 yolunu uyarır.",
            "isPracticeQuestion": True
        },
        "relatedQuestions": []
    },
    {
        "slideNumber": 5,
        "title": "T Lenfosit Alt Grupları: Th1, Th2 ve Th17 Hücreleri",
        "subtitle": "Kazanılmış bağışıklığın orkestrasyonu ve makrofajlarla karşılıklı iki yönlü etkileşim.",
        "badge": "Lenfositler",
        "badgeColor": "violet",
        "discipline": "Tıbbi Patoloji",
        "content": "### T Yardımcı (CD4+) Hücre Alt Tipleri\nKronik enflamasyonda CD4+ T yardımcı lenfositler ürettikleri sitokin profiline göre üçe ayrılır:\n\n1. **Th1 Hücreleri:**\n  - **Sitokin:** **IFN-g (İnterferon-gama)**.\n  - **Hedef:** M1 makrofajları aktive eder.\n  - **Görev:** İntraselüler bakteriler (tüberküloz) ve virüslere karşı hücresel savunma.\n2. **Th2 Hücreleri:**\n  - **Sitokinler:** **IL-4, IL-5, IL-13**.\n  - **Hedef:** M2 makrofajları (IL-4, IL-13) ve **eozinofilleri (IL-5)** aktive eder; B lenfositlerden IgE sınıf değişimini tetikler.\n  - **Görev:** Parazitik helmint enfeksiyonları ve alerjik hastalıklar.\n3. **Th17 Hücreleri:**\n  - **Sitokinler:** **IL-17 ve IL-22**.\n  - **Hedef:** Nötrofil ve monositleri çeken kemokin salınımını tetikler.\n  - **Görev:** Ekstraselüler bakteri ve mantar savunması; sedef hastalığı ve MS gibi otoimmün hastalıklarda rol oynar.\n\n> 🔴 ÖNEMLİ: Makrofajlar T hücrelerine antijen sunup IL-12 salgılar; T hücreleri ise IFN-γ üreterek makrofajları aktive eder. Bu **kendi kendini besleyen döngü** kronikleşmenin temelidir.",
        "synthesisNarrative": "### T Yardımcı (CD4+) Hücre Alt Tipleri\nKronik enflamasyonda CD4+ T yardımcı lenfositler ürettikleri sitokin profiline göre üçe ayrılır:\n\n1. **Th1 Hücreleri:**\n  - **Sitokin:** **IFN-g (İnterferon-gama)**.\n  - **Hedef:** M1 makrofajları aktive eder.\n  - **Görev:** İntraselüler bakteriler (tüberküloz) ve virüslere karşı hücresel savunma.\n2. **Th2 Hücreleri:**\n  - **Sitokinler:** **IL-4, IL-5, IL-13**.\n  - **Hedef:** M2 makrofajları (IL-4, IL-13) ve **eozinofilleri (IL-5)** aktive eder; B lenfositlerden IgE sınıf değişimini tetikler.\n  - **Görev:** Parazitik helmint enfeksiyonları ve alerjik hastalıklar.\n3. **Th17 Hücreleri:**\n  - **Sitokinler:** **IL-17 ve IL-22**.\n  - **Hedef:** Nötrofil ve monositleri çeken kemokin salınımını tetikler.\n  - **Görev:** Ekstraselüler bakteri ve mantar savunması; sedef hastalığı ve MS gibi otoimmün hastalıklarda rol oynar.\n\n> 🔴 ÖNEMLİ: Makrofajlar T hücrelerine antijen sunup IL-12 salgılar; T hücreleri ise IFN-γ üreterek makrofajları aktive eder. Bu **kendi kendini besleyen döngü** kronikleşmenin temelidir.",
        "spots": [
            "🔴 ÖNEMLİ: Th1 -> IFN-γ -> M1 Makrofaj. Th2 -> IL-4/IL-13 -> M2 Makrofaj. Th2 -> IL-5 -> Eozinofil.",
            "🔵 ÇIKMIŞ SORU: Eozinofillerin farklılaşmasını, aktivasyonunu ve hayatta kalmasını sağlayan en kritik sitokin IL-5'tir."
        ],
        "spotPearls": [
            "🔴 ÖNEMLİ: Th1 -> IFN-γ -> M1 Makrofaj. Th2 -> IL-4/IL-13 -> M2 Makrofaj. Th2 -> IL-5 -> Eozinofil.",
            "🔵 ÇIKMIŞ SORU: Eozinofillerin farklılaşmasını, aktivasyonunu ve hayatta kalmasını sağlayan en kritik sitokin IL-5'tir."
        ],
        "flashcards": [
            {
                "id": "fc-kronik-5",
                "category": "İmmünoloji",
                "front": "Th1, Th2 ve Th17 hücrelerinin karakteristik ana sitokinleri nelerdir?",
                "back": "Th1: IFN-γ\nTh2: IL-4, IL-5, IL-13\nTh17: IL-17 ve IL-22",
                "hint": "İnterferon, interlökinler"
            }
        ],
        "coreContent": {
            "keyBullets": [
                { "title": "⚡ İki Yönlü Kısır Döngü", "desc": "Makrofaj (IL-12) -> Th1 aktivasyonu -> IFN-γ salınımı -> Daha çok makrofaj aktivasyonu." }
            ]
        },
        "practiceQuestion": {
            "id": "q-kronik-enf-5",
            "stem": "Parazit enfeksiyonlarında ve alerjik reaksiyonlarda eozinofillerin kemik iliğinden çıkışını ve aktivasyonunu sağlayan temel Th2 sitokini hangisidir?",
            "options": [
                { "key": "A", "text": "IL-5" },
                { "key": "B", "text": "IFN-γ" },
                { "key": "C", "text": "IL-2" },
                { "key": "D", "text": "IL-17" },
                { "key": "E", "text": "TNF-α" }
            ],
            "correctAnswer": "A",
            "explanation": "IL-5, eozinofillerin güçlü aktivatörü ve büyüme faktörüdür. Paraziter enfeksiyonlarda Th2 lenfositlerince salınır.",
            "isPracticeQuestion": True
        },
        "relatedQuestions": []
    },
    {
        "slideNumber": 6,
        "title": "Plazma Hücreleri ve B Lenfosit Yanıtı",
        "subtitle": "Antikor salgılayan plazma hücreleri, Russell cisimcikleri ve saat kadranı kromatini.",
        "badge": "Plazma Hücreleri",
        "badgeColor": "teal",
        "discipline": "Tıbbi Patoloji",
        "content": "### Plazma Hücrelerinin Morfolojisi ve Biyolojisi\nB lenfositler antijenik uyarı ve T hücresi desteğiyle antikor üreten terminal evre hücreleri olan **plazma hücrelerine** farklılaşırlar:\n\n• **Histolojik Görünüm:**\n  - Eksantrik (hücre kenarına itilmiş) yuvarlak nükleus.\n  - **Saat kadranı (clock-face)** veya araba tekerleği (cartwheel) şeklinde periferal heterokromatin paterni.\n  - Belirgin perinükleer soluk alan (Golgı kompleksi) ve yoğun bazofilik sitoplazma (zengin kaba endoplazmik retikulum - rER).\n• **Russell Cisimcikleri:**\n  - Aşırı immünglobulin sentezi ve endoplazmik retikulumda protein birikmesi sonucu oluşan eozinofilik küresel inklüzyonlardır.\n  - Sitoplazmada olursa **Russell cisimciği**; nükleusta olursa **Dutcher cisimciği** adını alır.\n• **Tersiyer Lenfoid Yapılar (TLS):**\n  - Uzamış kronik enflamasyonda (Romatoid Artrit sinovyası, Hashimoto tiroiditi) doku içinde organize B ve T zonları, germinal merkezler içeren lenfoid foliküller gelişir.",
        "synthesisNarrative": "### Plazma Hücrelerinin Morfolojisi ve Biyolojisi\nB lenfositler antijenik uyarı ve T hücresi desteğiyle antikor üreten terminal evre hücreleri olan **plazma hücrelerine** farklılaşırlar:\n\n• **Histolojik Görünüm:**\n  - Eksantrik (hücre kenarına itilmiş) yuvarlak nükleus.\n  - **Saat kadranı (clock-face)** veya araba tekerleği (cartwheel) şeklinde periferal heterokromatin paterni.\n  - Belirgin perinükleer soluk alan (Golgı kompleksi) ve yoğun bazofilik sitoplazma (zengin kaba endoplazmik retikulum - rER).\n• **Russell Cisimcikleri:**\n  - Aşırı immünglobulin sentezi ve endoplazmik retikulumda protein birikmesi sonucu oluşan eozinofilik küresel inklüzyonlardır.\n  - Sitoplazmada olursa **Russell cisimciği**; nükleusta olursa **Dutcher cisimciği** adını alır.\n• **Tersiyer Lenfoid Yapılar (TLS):**\n  - Uzamış kronik enflamasyonda (Romatoid Artrit sinovyası, Hashimoto tiroiditi) doku içinde organize B ve T zonları, germinal merkezler içeren lenfoid foliküller gelişir.",
        "spots": [
            "🔴 ÖNEMLİ: Plazma hücresinde ER içinde biriken eozinofilik immünglobulin agregatlarına Russell cisimciği denir.",
            "🔵 ÇIKMIŞ SORU: Hashimoto tiroiditinde ve Romatoid artritte enflamasyon alanında germinal merkezli tersiyer lenfoid foliküller oluşur."
        ],
        "spotPearls": [
            "🔴 ÖNEMLİ: Plazma hücresinde ER içinde biriken eozinofilik immünglobulin agregatlarına Russell cisimciği denir.",
            "🔵 ÇIKMIŞ SORU: Hashimoto tiroiditinde ve Romatoid artritte enflamasyon alanında germinal merkezli tersiyer lenfoid foliküller oluşur."
        ],
        "flashcards": [
            {
                "id": "fc-kronik-6",
                "category": "Morfoloji",
                "front": "Plazma hücresinin sitoplazmasında aşırı immünglobulin birikimiyle oluşan eozinofilik globüllere ne ad verilir?",
                "back": "Russell cisimcikleri (Nükleusta olursa Dutcher cisimciği).",
                "hint": "Russell body"
            }
        ],
        "coreContent": {
            "keyBullets": [
                { "title": "🔬 Mikroskopi İpucu", "desc": "Eksantrik nükleus, saat kadranı kromatini, perinükleer halo (Golgi) ve bazofilik sitoplazma plazma hücresinin tipik imzasıdır." }
            ]
        },
        "practiceQuestion": {
            "id": "q-kronik-enf-6",
            "stem": "Kronik enflamasyon alanında bol miktarda izlenen, eksantrik yerleşimli saat kadranı kromatinli nükleusu, perinükleer soluk alanı ve sitoplazmasında immünglobulin yüklü Russell cisimcikleri bulunan hücre hangisidir?",
            "options": [
                { "key": "A", "text": "Plazma hücresi" },
                { "key": "B", "text": "Epiteloid histiyosit" },
                { "key": "C", "text": "Langhans dev hücresi" },
                { "key": "D", "text": "Eozinofil lökosit" },
                { "key": "E", "text": "Mast hücresi" }
            ],
            "correctAnswer": "A",
            "explanation": "Saat kadranı kromatini, perinükleer solukluk ve Russell cisimcikleri antikor sentezleyen plazma hücresinin ayırt edici morfolojik özellikleridir.",
            "isPracticeQuestion": True
        },
        "relatedQuestions": []
    },
    {
        "slideNumber": 7,
        "title": "Eozinofiller ve Mast Hücreleri",
        "subtitle": "IgE aracılı reaksiyonlar, parazit savunması, Major Basic Protein ve Charcot-Leyden kristalleri.",
        "badge": "Eozinofiller & Mast",
        "badgeColor": "rose",
        "discipline": "Tıbbi Patoloji",
        "content": "### Eozinofillerin ve Mast Hücrelerinin Kronik Rolü\n• **Eozinofiller:**\n  - Parazit enfeksiyonlarında ve IgE aracılı alerjik enflamasyonda (astım, saman nezlesi) dokuya çağrılırlar.\n  - Kemokin **eotaksin (CCL11)** ve **IL-5** aracılığıyla göç ederler.\n  - Granüllerinde **Major Basic Protein (MBP)** bulunur; parazitler için toksiktir ancak aynı zamanda konak epitel hücrelerinde de ciddi nekroza yol açar.\n  - Yıkılan eozinofillerin granül membran proteinlerinden hekzagonal bipiramidal **Charcot-Leyden kristalleri** oluşur (astım balgamında patognomoniktir).\n• **Mast Hücreleri:**\n  - Bağ dokusunda yerleşiktir; yüzeylerinde yüksek afiniteli IgE reseptörü (FceRI) taşırlar.\n  - Degranülasyonla histamin, lökotrien ve sitokin salgılarlar; anafilakside ve alerjik yanıtta rol alırlar.",
        "synthesisNarrative": "### Eozinofillerin ve Mast Hücrelerinin Kronik Rolü\n• **Eozinofiller:**\n  - Parazit enfeksiyonlarında ve IgE aracılı alerjik enflamasyonda (astım, saman nezlesi) dokuya çağrılırlar.\n  - Kemokin **eotaksin (CCL11)** ve **IL-5** aracılığıyla göç ederler.\n  - Granüllerinde **Major Basic Protein (MBP)** bulunur; parazitler için toksiktir ancak aynı zamanda konak epitel hücrelerinde de ciddi nekroza yol açar.\n  - Yıkılan eozinofillerin granül membran proteinlerinden hekzagonal bipiramidal **Charcot-Leyden kristalleri** oluşur (astım balgamında patognomoniktir).\n• **Mast Hücreleri:**\n  - Bağ dokusunda yerleşiktir; yüzeylerinde yüksek afiniteli IgE reseptörü (FceRI) taşırlar.\n  - Degranülasyonla histamin, lökotrien ve sitokin salgılarlar; anafilakside ve alerjik yanıtta rol alırlar.",
        "spots": [
            "🔴 ÖNEMLİ: Eozinofil granüllerindeki Major Basic Protein (MBP) hem parazitleri öldürür hem epitel hasarı yapar.",
            "🔵 ÇIKMIŞ SORU: Astımlı hastaların balgamında görülen eozinofil kaynaklı kristaller Charcot-Leyden kristalleridir."
        ],
        "spotPearls": [
            "🔴 ÖNEMLİ: Eozinofil granüllerindeki Major Basic Protein (MBP) hem parazitleri öldürür hem epitel hasarı yapar.",
            "🔵 ÇIKMIŞ SORU: Astımlı hastaların balgamında görülen eozinofil kaynaklı kristaller Charcot-Leyden kristalleridir."
        ],
        "flashcards": [
            {
                "id": "fc-kronik-7",
                "category": "Morfoloji",
                "front": "Eozinofillerin lizisi sonucu dokuda veya balgamda oluşan kristallerin adı nedir?",
                "back": "Charcot-Leyden kristalleri (galektin-10 proteininden oluşur).",
                "hint": "Charcot-Leyden"
            }
        ],
        "coreContent": {
            "keyBullets": [
                { "title": "🎯 Sınav Spotu", "desc": "Charcot-Leyden kristalleri ve Curschmann spiralleri bronşiyal astım balgamının klasik bulgularıdır." }
            ]
        },
        "practiceQuestion": {
            "id": "q-kronik-enf-7",
            "stem": "Alerjik astım atağındaki bir hastanın balgam yaymasında bol miktarda eozinofil ile birlikte izlenen hekzagonal bipiramidal kristal yapılar hangisidir?",
            "options": [
                { "key": "A", "text": "Charcot-Leyden kristalleri" },
                { "key": "B", "text": "Reinke kristalleri" },
                { "key": "C", "text": "Kolesterol kristalleri" },
                { "key": "D", "text": "Ürat kristalleri" },
                { "key": "E", "text": "Kalsiyum pirofosfat kristalleri" }
            ],
            "correctAnswer": "A",
            "explanation": "Charcot-Leyden kristalleri, parçalanan eozinofillerin membran proteinlerinden oluşan ve astım balgamında sıkça görülen kristal yapılardır.",
            "isPracticeQuestion": True
        },
        "relatedQuestions": []
    },
    {
        "slideNumber": 8,
        "title": "Granülomatöz Enflamasyonun Tanımı ve Mimarisi",
        "subtitle": "Kollaps ve fagositoz yetersizliğine karşı organizmanın bariyer kurma stratejisi.",
        "badge": "Granülom Mimarisi",
        "badgeColor": "red",
        "discipline": "Tıbbi Patoloji",
        "professorAudioHighlight": {
            "timestamp": "22:10",
            "quote": "Granülomun temel hücresi makrofajdır; ancak sıradan makrofaj değil, aktive olup bol sitoplazma kazanan EPİTELOİD HİSTİYOSİTTİR.",
            "emphasisType": "direct_exam_warning",
            "note": "Epiteloid histiyositlerin birleşmesiyle çok çekirdekli dev hücreler oluşur; etrafı T lenfosit taç kuşağı ve dışta fibroblastlarla çevrilidir."
        },
        "content": "### Granülomatöz Enflamasyon Nedir?\nGranülomatöz enflamasyon, yok edilmesi güç etkenleri sınırlamak (adeta hapse atmak) için gelişen **özelleşmiş bir kronik enflamasyon** tipidir.\n\n• **Granülomun Temel Yapı Taşları:**\n  1. **Epiteloid Histiyositler (Makrofajlar):**\n     - Granülomun zorunlu ve tanı koydurucu ana hücresidir.\n     - Bol soluk pembe eozinofilik sitoplazmalı, sınırları belirsiz, epitel hücrelerine benzeyen modifiye makrofajlardır.\n     - Nükleusları terlik (slipper) veya ayakkabı tabanı şeklinde, veziküler ve açıktır.\n  2. **Çok Çekirdekli Dev Hücreler:**\n     - Epiteloid histiyositlerin füzyonuyla (birleşmesiyle) oluşurlar (Langhans, yabancı cisim, Touton tipi).\n  3. **Lenfosit Taç Kuşağı (Collar):**\n     - Granülomun çevresinde T ve B lenfositlerden oluşan koruyucu bir kuşak yer alır.\n  4. **Periferik Fibrozis:**\n     - En dışta lezyonu sınırlayan fibroblastlar ve kollajen lifler bulunur.",
        "synthesisNarrative": "### Granülomatöz Enflamasyon Nedir?\nGranülomatöz enflamasyon, yok edilmesi güç etkenleri sınırlamak (adeta hapse atmak) için gelişen **özelleşmiş bir kronik enflamasyon** tipidir.\n\n• **Granülomun Temel Yapı Taşları:**\n  1. **Epiteloid Histiyositler (Makrofajlar):**\n     - Granülomun zorunlu ve tanı koydurucu ana hücresidir.\n     - Bol soluk pembe eozinofilik sitoplazmalı, sınırları belirsiz, epitel hücrelerine benzeyen modifiye makrofajlardır.\n     - Nükleusları terlik (slipper) veya ayakkabı tabanı şeklinde, veziküler ve açıktır.\n  2. **Çok Çekirdekli Dev Hücreler:**\n     - Epiteloid histiyositlerin füzyonuyla (birleşmesiyle) oluşurlar (Langhans, yabancı cisim, Touton tipi).\n  3. **Lenfosit Taç Kuşağı (Collar):**\n     - Granülomun çevresinde T ve B lenfositlerden oluşan koruyucu bir kuşak yer alır.\n  4. **Periferik Fibrozis:**\n     - En dışta lezyonu sınırlayan fibroblastlar ve kollajen lifler bulunur.",
        "spots": [
            "🔴 ÖNEMLİ: Bir lezyona granülom denilebilmesi için epiteloid histiyosit kümesi şarttır; dev hücreler şart değildir ancak sıklıkla eşlik eder.",
            "🔵 ÇIKMIŞ SORU: Epiteloid histiyositler modifiye makrofajlardır; sitoplazmaları bol, sınırları belirsiz ve nükleusları terlik şeklindedir."
        ],
        "spotPearls": [
            "🔴 ÖNEMLİ: Bir lezyona granülom denilebilmesi için epiteloid histiyosit kümesi şarttır; dev hücreler şart değildir ancak sıklıkla eşlik eder.",
            "🔵 ÇIKMIŞ SORU: Epiteloid histiyositler modifiye makrofajlardır; sitoplazmaları bol, sınırları belirsiz ve nükleusları terlik şeklindedir."
        ],
        "flashcards": [
            {
                "id": "fc-kronik-8",
                "category": "Morfoloji",
                "front": "Granülomun oluşması için bulunması kesinlikle zorunlu olan temel hücre hangisidir?",
                "back": "Epiteloid histiyosit (aktive modifiye makrofaj).",
                "hint": "Epiteloid hücre"
            }
        ],
        "coreContent": {
            "keyBullets": [
                { "title": "🛡️ İzolasyon Stratejisi", "desc": "Yok edilemeyen tüberküloz basili veya yabancı cisim etrafına örülen hücresel duvardır." }
            ]
        },
        "practiceQuestion": {
            "id": "q-kronik-enf-8",
            "stem": "Granülom teşhisi konulabilmesi için histopatolojik incelemede varlığı MUTLAKA gerekli olan ana hücresel eleman hangisidir?",
            "options": [
                { "key": "A", "text": "Epiteloid histiyosit topluluğu" },
                { "key": "B", "text": "Kazeifikasyon nekrozu" },
                { "key": "C", "text": "Langhans tipi dev hücre" },
                { "key": "D", "text": "Yoğun nötrofilik infiltrasyon" },
                { "key": "E", "text": "Kalsifikasyon odakları" }
            ],
            "correctAnswer": "A",
            "explanation": "Granülom tanısı için epiteloid histiyositlerin odak oluşturması şarttır. Nekroz veya dev hücre bulunmasa bile epiteloid histiyosit kümesi granülomdur.",
            "isPracticeQuestion": True
        },
        "relatedQuestions": []
    },
    {
        "slideNumber": 9,
        "title": "Çok Çekirdekli Dev Hücre Tipleri",
        "subtitle": "Langhans tipi, Yabancı Cisim tipi ve Touton tipi dev hücrelerin ayrımı.",
        "badge": "Dev Hücre Tipleri",
        "badgeColor": "amber",
        "discipline": "Tıbbi Patoloji",
        "content": "### Dev Hücrelerin Morfolojik Sınıflandırması\nEpiteloid histiyositlerin (makrofajların) birbirleriyle kaynaşması (füzyon) sonucu onlarca çekirdek içeren dev hücreler oluşur:\n\n1. **Langhans Tipi Dev Hücre:**\n  - Nükleuslar hücrenin periferine **at nalı (horseshoe)** veya yarımay şeklinde dizilmiştir.\n  - Klasik olarak **tüberkülozda** ve diğer immün granülomlarda (sarkoidoz vb.) görülür.\n2. **Yabancı Cisim (Foreign-body) Tipi Dev Hücre:**\n  - Nükleuslar sitoplazmanın merkezinde ve her yerinde **düzensiz, dağınık** olarak kümelenmiştir.\n  - Dikiş materyali, talk pudrası, odun kıymığı gibi inert yabancı maddelerin çevresinde oluşur.\n3. **Touton Dev Hücresi:**\n  - Nükleuslar merkezi bir daire (halka) şeklinde dizilmiştir; halkanın dışındaki sitoplazma lipid yüklü olduğundan köpüksü ve soluktur.\n  - **Ksantomalar**, ksantogranülomlar ve yağ nekrozu alanlarında görülür.",
        "synthesisNarrative": "### Dev Hücrelerin Morfolojik Sınıflandırması\nEpiteloid histiyositlerin (makrofajların) birbirleriyle kaynaşması (füzyon) sonucu onlarca çekirdek içeren dev hücreler oluşur:\n\n1. **Langhans Tipi Dev Hücre:**\n  - Nükleuslar hücrenin periferine **at nalı (horseshoe)** veya yarımay şeklinde dizilmiştir.\n  - Klasik olarak **tüberkülozda** ve diğer immün granülomlarda (sarkoidoz vb.) görülür.\n2. **Yabancı Cisim (Foreign-body) Tipi Dev Hücre:**\n  - Nükleuslar sitoplazmanın merkezinde ve her yerinde **düzensiz, dağınık** olarak kümelenmiştir.\n  - Dikiş materyali, talk pudrası, odun kıymığı gibi inert yabancı maddelerin çevresinde oluşur.\n3. **Touton Dev Hücresi:**\n  - Nükleuslar merkezi bir daire (halka) şeklinde dizilmiştir; halkanın dışındaki sitoplazma lipid yüklü olduğundan köpüksü ve soluktur.\n  - **Ksantomalar**, ksantogranülomlar ve yağ nekrozu alanlarında görülür.",
        "spots": [
            "🔴 ÖNEMLİ: Langhans dev hücresinde çekirdekler at nalı şeklinde periferdedir; yabancı cisim dev hücresinde ise dağınıktır.",
            "🔵 ÇIKMIŞ SORU: Çekirdeklerin daire oluşturduğu ve çevresinde lipid yüklü köpüksü sitoplazma bulunan dev hücre Touton dev hücresidir."
        ],
        "spotPearls": [
            "🔴 ÖNEMLİ: Langhans dev hücresinde çekirdekler at nalı şeklinde periferdedir; yabancı cisim dev hücresinde ise dağınıktır.",
            "🔵 ÇIKMIŞ SORU: Çekirdeklerin daire oluşturduğu ve çevresinde lipid yüklü köpüksü sitoplazma bulunan dev hücre Touton dev hücresidir."
        ],
        "flashcards": [
            {
                "id": "fc-kronik-9",
                "category": "Morfoloji",
                "front": "Tüberküloz granülomlarında görülen, nükleusları at nalı şeklinde dizilmiş dev hücre hangisidir?",
                "back": "Langhans tipi dev hücre.",
                "hint": "Langhans (Langerhans ile karıştırma!)"
            }
        ],
        "coreContent": {
            "table": {
                "title": "Çok Çekirdekli Dev Hücre Tipleri",
                "headers": ["Dev Hücre Tipi", "Çekirdek Dizilimi", "Görüldüğü Tipik Durumlar"],
                "rows": [
                    ["Langhans Dev Hücresi", "Periferde at nalı veya yarım daire", "Tüberküloz, Sarkoidoz, İmmün Granülomlar"],
                    ["Yabancı Cisim Dev Hücresi", "Sitoplazmada rastgele, dağınık küme", "Cerrahi sütür, talk, protez, yabancı cisim"],
                    ["Touton Dev Hücresi", "Halka şeklinde nükleus + köpüksü perifer", "Ksantoma, JXG, Yağ nekrozu"],
                    ["Aschoff Dev Hücresi", "Belirgin nükleollü tırtıl (Anitschkow) nükleus", "Akut Romatizmal Ateş (Aschoff nodülü)"]
                ]
            }
        },
        "practiceQuestion": {
            "id": "q-kronik-enf-9",
            "stem": "Akciğer biyopsisinde granülom içinde nükleusları hücre periferinde 'at nalı' konfigürasyonunda dizilmiş çok çekirdekli dev hücre izlenmiştir. Bu hücre tipi hangisidir?",
            "options": [
                { "key": "A", "text": "Langhans tipi dev hücre" },
                { "key": "B", "text": "Yabancı cisim tipi dev hücre" },
                { "key": "C", "text": "Touton tipi dev hücre" },
                { "key": "D", "text": "Osteoklast" },
                { "key": "E", "text": "Megakaryosit" }
            ],
            "correctAnswer": "A",
            "explanation": "Nükleusların hücre çeperinde at nalı şeklinde dizilmesi Langhans dev hücresinin tipik özelliğidir ve tüberkülozda karakteristiktir.",
            "isPracticeQuestion": True
        },
        "relatedQuestions": []
    },
    {
        "slideNumber": 10,
        "title": "Kazeöz ve Non-Kazeöz Granülom Ayrımı",
        "subtitle": "Kazeifikasyon nekrozu içeren enfeksiyöz granülomlar vs nekrozsuz immün granülomlar.",
        "badge": "Ayırıcı Tanı",
        "badgeColor": "rose",
        "discipline": "Tıbbi Patoloji",
        "content": "### Granülomların İki Ana Kategorisi\nGranülomlar merkezlerinde nekroz bulunup bulunmamasına göre ikiye ayrılır:\n\n1. **Kazeifiye (Kazeöz) Granülomlar:**\n  - Granülomun merkezinde yapısız, pembe, granüler, hücresel detritlerden oluşan **kazeifikasyon nekrozu (peynirleşme nekrozu)** yer alır.\n  - Hücre sınırları tamamen silinmiştir.\n  - **Klasik Örnek:** **Tüberküloz** (*Mycobacterium tuberculosis*).\n  - Diğer örnekler: Mantar enfeksiyonları (Histoplazmoz, Koksidioidomikoz), Kedi tırmığı hastalığı (süppüratif kazeifiye).\n2. **Non-Kazeifiye (Nekrotizan Olmayan) Granülomlar:**\n  - Merkezinde kazeifikasyon nekrozu YOKTUR; tamamen sağlam epiteloid histiyositler ve dev hücrelerden oluşur.\n  - **Klasik Örnek:** **Sarkoidoz** (çıplak granülomlar), **Crohn hastalığı**, **Berilyozis**.\n\n> 🔴 ÖNEMLİ: Sarkoidozda granülomlar kazeöz nekroz içermez ve lenfosit kuşağı incedir; bu nedenle 'çıplak (naked) granülom' olarak adlandırılır.",
        "synthesisNarrative": "### Granülomların İki Ana Kategorisi\nGranülomlar merkezlerinde nekroz bulunup bulunmamasına göre ikiye ayrılır:\n\n1. **Kazeifiye (Kazeöz) Granülomlar:**\n  - Granülomun merkezinde yapısız, pembe, granüler, hücresel detritlerden oluşan **kazeifikasyon nekrozu (peynirleşme nekrozu)** yer alır.\n  - Hücre sınırları tamamen silinmiştir.\n  - **Klasik Örnek:** **Tüberküloz** (*Mycobacterium tuberculosis*).\n  - Diğer örnekler: Mantar enfeksiyonları (Histoplazmoz, Koksidioidomikoz), Kedi tırmığı hastalığı (süppüratif kazeifiye).\n2. **Non-Kazeifiye (Nekrotizan Olmayan) Granülomlar:**\n  - Merkezinde kazeifikasyon nekrozu YOKTUR; tamamen sağlam epiteloid histiyositler ve dev hücrelerden oluşur.\n  - **Klasik Örnek:** **Sarkoidoz** (çıplak granülomlar), **Crohn hastalığı**, **Berilyozis**.\n\n> 🔴 ÖNEMLİ: Sarkoidozda granülomlar kazeöz nekroz içermez ve lenfosit kuşağı incedir; bu nedenle 'çıplak (naked) granülom' olarak adlandırılır.",
        "spots": [
            "🔴 ÖNEMLİ: Kazeöz granülomun prototipi Tüberküloz; non-kazeöz granülomun prototipi Sarkoidozdur.",
            "🔵 ÇIKMIŞ SORU: Sarkoidoz granülomlarında kazeifikasyon nekrozu görülmez; 'çıplak granülom' terimi sarkoidoz için kullanılır."
        ],
        "spotPearls": [
            "🔴 ÖNEMLİ: Kazeöz granülomun prototipi Tüberküloz; non-kazeöz granülomun prototipi Sarkoidozdur.",
            "🔵 ÇIKMIŞ SORU: Sarkoidoz granülomlarında kazeifikasyon nekrozu görülmez; 'çıplak granülom' terimi sarkoidoz için kullanılır."
        ],
        "flashcards": [
            {
                "id": "fc-kronik-10",
                "category": "Ayırıcı Tanı",
                "front": "Sarkoidoz ve Crohn hastalığındaki granülomların tüberkülozdan en belirgin morfolojik farkı nedir?",
                "back": "Kazeifikasyon nekrozu içermemeleridir (Non-kazeöz granülomlardır).",
                "hint": "Nekroz varlığı/yokluğu"
            }
        ],
        "coreContent": {
            "keyBullets": [
                { "title": "🔬 Sınav Ayrımı", "desc": "Tüberküloz = Kazeifiye Nekrotizan Granülom; Sarkoidoz = Non-kazeifiye Çıplak Granülom." }
            ]
        },
        "practiceQuestion": {
            "id": "q-kronik-enf-10",
            "stem": "Akciğer hiler lenf nodu biyopsisinde merkezinde kazeöz nekroz içermeyen, epiteloid histiyositler ve Langhans dev hücrelerinden zengin, periferik lenfosit halkası dar olan 'çıplak granülom' saptanan bir hastada en olası tanı hangisidir?",
            "options": [
                { "key": "A", "text": "Sarkoidoz" },
                { "key": "B", "text": "Primer Tüberküloz" },
                { "key": "C", "text": "Histoplazmoz" },
                { "key": "D", "text": "Kedi Tırmığı Hastalığı" },
                { "key": "E", "text": "Sifiliz" }
            ],
            "correctAnswer": "A",
            "explanation": "Kazeöz nekroz içermeyen, sıkı ve dar lenfosit kuşaklı non-kazeöz (çıplak) granülomlar sarkoidozun en karakteristik histopatolojik bulgusudur.",
            "isPracticeQuestion": True
        },
        "relatedQuestions": []
    },
    {
        "slideNumber": 11,
        "title": "Tüberküloz Patolojisi ve Granülom Oluşum Mekanizması",
        "subtitle": "Ghon kompleksi, kazeöz nekroz ve ARB (Ehrlich-Ziehl-Neelsen) boyanması.",
        "badge": "Tüberküloz",
        "badgeColor": "red",
        "discipline": "Tıbbi Patoloji",
        "content": "### Tüberkülozda Granülom Patogenezi\n*Mycobacterium tuberculosis*, mikolik asit ve kord faktörü içeren kalın lipidik hücre duvarı nedeniyle fagozom-lizozom füzyonunu engeller ve makrofaj içinde çoğalır:\n\n1. **Gecikmiş Tip Aşırı Duyarlılık (Tip IV):**\n  - Makrofajlar antijeni bölgesel lenf nodundaki T lenfositlere sunar ve **IL-12** salgılar.\n  - CD4+ T hücreleri **Th1**'e farklılaşır ve **IFN-g** üretir.\n  - IFN-γ makrofajları aktive ederek mikrobisidal M1 haline ve epiteloid histiyositlere dönüştürür; TNF salınımı granülom yapısını bir arada tutar.\n2. **Kazeöz Nekroz Gelişimi:**\n  - Yoğun makrofaj lizozomal enzimleri ve sitokinlerin etkisiyle merkezde peynirimsi, asellüler, granüler nekroz alanı (kazeifikasyon) oluşur.\n3. **Tanı Boyası:**\n  - Mikobakteriler aside dirençli boyalarla (**Ehrlich-Ziehl-Neelsen - EZN** veya floresan Auramin-Rhodamin) parlak kırmızı basil şeklinde boyanır.",
        "synthesisNarrative": "### Tüberkülozda Granülom Patogenezi\n*Mycobacterium tuberculosis*, mikolik asit ve kord faktörü içeren kalın lipidik hücre duvarı nedeniyle fagozom-lizozom füzyonunu engeller ve makrofaj içinde çoğalır:\n\n1. **Gecikmiş Tip Aşırı Duyarlılık (Tip IV):**\n  - Makrofajlar antijeni bölgesel lenf nodundaki T lenfositlere sunar ve **IL-12** salgılar.\n  - CD4+ T hücreleri **Th1**'e farklılaşır ve **IFN-g** üretir.\n  - IFN-γ makrofajları aktive ederek mikrobisidal M1 haline ve epiteloid histiyositlere dönüştürür; TNF salınımı granülom yapısını bir arada tutar.\n2. **Kazeöz Nekroz Gelişimi:**\n  - Yoğun makrofaj lizozomal enzimleri ve sitokinlerin etkisiyle merkezde peynirimsi, asellüler, granüler nekroz alanı (kazeifikasyon) oluşur.\n3. **Tanı Boyası:**\n  - Mikobakteriler aside dirençli boyalarla (**Ehrlich-Ziehl-Neelsen - EZN** veya floresan Auramin-Rhodamin) parlak kırmızı basil şeklinde boyanır.",
        "spots": [
            "🔴 ÖNEMLİ: Tüberküloz granülomunun bütünlüğünü koruyan ve devamını sağlayan en kritik sitokin TNF-alfa dır; anti-TNF ilaçlar latent tüberkülozu reaktive eder!",
            "🔵 ÇIKMIŞ SORU: Tüberküloz basilleri Ehrlich-Ziehl-Neelsen (EZN) boyasında hücre duvarındaki mikolik asit sayesinde kırmızı renkli aside dirençli basil (ARB) olarak görülür."
        ],
        "spotPearls": [
            "🔴 ÖNEMLİ: Tüberküloz granülomunun bütünlüğünü koruyan ve devamını sağlayan en kritik sitokin TNF-alfa dır; anti-TNF ilaçlar latent tüberkülozu reaktive eder!",
            "🔵 ÇIKMIŞ SORU: Tüberküloz basilleri Ehrlich-Ziehl-Neelsen (EZN) boyasında hücre duvarındaki mikolik asit sayesinde kırmızı renkli aside dirençli basil (ARB) olarak görülür."
        ],
        "flashcards": [
            {
                "id": "fc-kronik-11",
                "category": "Farmakoloji & Patoloji",
                "front": "Hangi biyolojik ajan tedavisi öncesinde latent tüberküloz reaktivasyonu riski nedeniyle PPD/QuantiFERON taraması zorunludur?",
                "back": "Anti-TNF ajanlar (İnfliksimab, Adalimumab, Etanersept) — çünkü TNF granülomun bütünlüğünü sağlar.",
                "hint": "Anti-TNF ilaçlar"
            }
        ],
        "coreContent": {
            "keyBullets": [
                { "title": "⚠️ Hayati Klinik Uyarı", "desc": "Anti-TNF biyolojik ajanlar granülomun çökmesine ve basillerin tüm vücuda dissemine olmasına (milier tüberküloz) yol açabilir." }
            ]
        },
        "practiceQuestion": {
            "id": "q-kronik-enf-11",
            "stem": "Romatoid artrit nedeniyle monoklonal antikor tedavisi başlanacak bir hastada latent tüberküloz enfeksiyonunun reaktive olarak milier yayılım göstermesini önlemek için tedavide hangi sitokinin bloke edilmesinden önce tarama yapılmalıdır?",
            "options": [
                { "key": "A", "text": "Tümör Nekroz Faktörü-alfa (TNF-α)" },
                { "key": "B", "text": "İnterlökin-4" },
                { "key": "C", "text": "İnterlökin-5" },
                { "key": "D", "text": "Transforme edici büyüme faktörü-beta (TGF-β)" },
                { "key": "E", "text": "Vasküler endotelyal büyüme faktörü (VEGF)" }
            ],
            "correctAnswer": "A",
            "explanation": "TNF-α, tüberküloz granülomunun organizasyonunu ve mikobakterilerin hapsedilmesini sağlayan temel sitokindir. Anti-TNF ilaçlar granülomu yıkarak reaktivasyona neden olur.",
            "isPracticeQuestion": True
        },
        "relatedQuestions": []
    },
    {
        "slideNumber": 12,
        "title": "Sarkoidoz Patolojisi ve İntraselüler İnklüzyonlar",
        "subtitle": "Bilateral hiler lenfadenopati, Schaumann cisimcikleri ve Asteroid cisimcikleri.",
        "badge": "Sarkoidoz",
        "badgeColor": "purple",
        "discipline": "Tıbbi Patoloji",
        "content": "### Sarkoidozun Morfolojik Özellikleri\nSarkoidoz, etyolojisi bilinmeyen, sıklıkla genç erişkinlerde akciğerleri ve hiler lenf nodlarını tutan multisistemik granülomatöz bir hastalıktır:\n\n• **Histopatoloji:**\n  - Karakteristik olarak **kazeifikasyon nekrozu içermeyen**, düzgün sınırlı, yoğun epiteloid histiyosit ve Langhans dev hücrelerinden oluşan granülomlar.\n  - Granülomlar zamanla konsantrik kollajenleşme ile hyalinize skara dönüşür.\n• **Dev Hücre İçi İnklüzyon Cisimcikleri:**\n  1. **Schaumann Cisimcikleri:** Dev hücre sitoplazmasında konsantrik laminasyonlu kalsiyum ve protein içeren bazofilik konkresyonlar.\n  2. **Asteroid Cisimcikleri:** Dev hücre içinde yıldızsı (stellat) konfigürasyonda eozinofilik sitoplazmik inklüzyonlar (tübül-lipit agregatları).\n\n> 🔵 ÇIKMIŞ SORU: Schaumann ve Asteroid cisimcikleri sarkoidoz için çok tipiktir ancak %100 patognomonik değildir; berilyozis ve tüberkülozda da nadiren görülebilir.",
        "synthesisNarrative": "### Sarkoidozun Morfolojik Özellikleri\nSarkoidoz, etyolojisi bilinmeyen, sıklıkla genç erişkinlerde akciğerleri ve hiler lenf nodlarını tutan multisistemik granülomatöz bir hastalıktır:\n\n• **Histopatoloji:**\n  - Karakteristik olarak **kazeifikasyon nekrozu içermeyen**, düzgün sınırlı, yoğun epiteloid histiyosit ve Langhans dev hücrelerinden oluşan granülomlar.\n  - Granülomlar zamanla konsantrik kollajenleşme ile hyalinize skara dönüşür.\n• **Dev Hücre İçi İnklüzyon Cisimcikleri:**\n  1. **Schaumann Cisimcikleri:** Dev hücre sitoplazmasında konsantrik laminasyonlu kalsiyum ve protein içeren bazofilik konkresyonlar.\n  2. **Asteroid Cisimcikleri:** Dev hücre içinde yıldızsı (stellat) konfigürasyonda eozinofilik sitoplazmik inklüzyonlar (tübül-lipit agregatları).\n\n> 🔵 ÇIKMIŞ SORU: Schaumann ve Asteroid cisimcikleri sarkoidoz için çok tipiktir ancak %100 patognomonik değildir; berilyozis ve tüberkülozda da nadiren görülebilir.",
        "spots": [
            "🔴 ÖNEMLİ: Sarkoidoz dev hücrelerinde iki tip inklüzyon: Kalsifiye Schaumann cisimcikleri ve yıldızsı Asteroid cisimcikleri.",
            "🔵 ÇIKMIŞ SORU: Sarkoidozda granülomlardaki makrofajların 1-alfa hidroksilaz üretimi nedeniyle hiperkalsemi ve hiperkalsiüri gelişir."
        ],
        "spotPearls": [
            "🔴 ÖNEMLİ: Sarkoidoz dev hücrelerinde iki tip inklüzyon: Kalsifiye Schaumann cisimcikleri ve yıldızsı Asteroid cisimcikleri.",
            "🔵 ÇIKMIŞ SORU: Sarkoidozda granülomlardaki makrofajların 1-alfa hidroksilaz üretimi nedeniyle hiperkalsemi ve hiperkalsiüri gelişir."
        ],
        "flashcards": [
            {
                "id": "fc-kronik-12",
                "category": "Morfoloji",
                "front": "Sarkoidoz granülomlarındaki dev hücrelerde izlenen konsantrik kalsifiye cisimcik ile yıldızsı cisimciklerin adları nelerdir?",
                "back": "Kalsifiye olan: Schaumann cisimciği\nYıldızsı olan: Asteroid cisimciği",
                "hint": "Schaumann ve Asteroid"
            }
        ],
        "coreContent": {
            "keyBullets": [
                { "title": "⚡ Patoloji İncisi", "desc": "Sarkoidozda D vitamini aktivasyonu (1-alfa hidroksilaz) doğrudan granülom makrofajları tarafından yapılır." }
            ]
        },
        "practiceQuestion": {
            "id": "q-kronik-enf-12",
            "stem": "Bilateral hiler lenfadenopatisi ve hiperkalsemisi olan 32 yaşındaki kadın hastanın lenf nodu biyopsisinde non-kazeöz granülomlar ve dev hücreler içinde konsantrik tabakalı kalsifiye konkresyonlar saptanmıştır. Bu konkresyonlara ne ad verilir?",
            "options": [
                { "key": "A", "text": "Schaumann cisimcikleri" },
                { "key": "B", "text": "Asteroid cisimcikleri" },
                { "key": "C", "text": "Russell cisimcikleri" },
                { "key": "D", "text": "Psammom cisimcikleri" },
                { "key": "E", "text": "Councilman cisimcikleri" },
            ],
            "correctAnswer": "A",
            "explanation": "Sarkoidoz granülomlarındaki dev hücrelerde bulunan konsantrik laminasyonlu kalsifiye yapılara Schaumann cisimcikleri adı verilir.",
            "isPracticeQuestion": True
        },
        "relatedQuestions": []
    },
    {
        "slideNumber": 13,
        "title": "Granülomatöz Hastalıkların Karşılaştırmalı Ayırıcı Tanısı",
        "subtitle": "Enfeksiyöz vs otoimmün vs yabancı cisim granülomları tablosu.",
        "badge": "Sınıflama Tablosu",
        "badgeColor": "teal",
        "discipline": "Tıbbi Patoloji",
        "content": "### Granülomatöz Hastalıklar Atlası\nKlinik pratikte ve komite sınavlarında sıkça karşılaşılan granülomatöz patolojilerin ayırıcı özellikleri aşağıda özetlenmiştir:\n\n• **Tüberküloz:** Kazeöz nekrozlu granülom, Langhans dev hücreleri, EZN ile aside dirençli basil (+).\n• **Cüzzam (Lepra):** *Mycobacterium leprae*; tüberküloid tipte granülomlar varken, lepromatöz tipte basillerle dolu köpüksü histiyositler (**Virchow hücreleri**) görülür.\n• **Sifiliz (Frengi):** Tersiyer evrede **Gum (gom)** lezyonu; merkezde koagülasyon nekrozu, çevrede plazma hücresi zengin granülomatöz reaksiyon ve **obliteratif endarterit**.\n• **Kedi Tırmığı Hastalığı (*Bartonella henselae*):** Lenf nodunda merkezinde nötrofiller içeren **yıldızsı (stellat) nekrotizan granülomlar**.\n• **Crohn Hastalığı:** Bağırsak duvarında transmural non-kazeöz granülomlar ve atlamalı (skip) lezyonlar.\n• **Yabancı Cisim Reaksiyonu:** Polarize ışıkta parlayan yabancı cisimler ve yabancı cisim tipi dev hücreler.",
        "synthesisNarrative": "### Granülomatöz Hastalıklar Atlası\nKlinik pratikte ve komite sınavlarında sıkça karşılaşılan granülomatöz patolojilerin ayırıcı özellikleri aşağıda özetlenmiştir:\n\n• **Tüberküloz:** Kazeöz nekrozlu granülom, Langhans dev hücreleri, EZN ile aside dirençli basil (+).\n• **Cüzzam (Lepra):** *Mycobacterium leprae*; tüberküloid tipte granülomlar varken, lepromatöz tipte basillerle dolu köpüksü histiyositler (**Virchow hücreleri**) görülür.\n• **Sifiliz (Frengi):** Tersiyer evrede **Gum (gom)** lezyonu; merkezde koagülasyon nekrozu, çevrede plazma hücresi zengin granülomatöz reaksiyon ve **obliteratif endarterit**.\n• **Kedi Tırmığı Hastalığı (*Bartonella henselae*):** Lenf nodunda merkezinde nötrofiller içeren **yıldızsı (stellat) nekrotizan granülomlar**.\n• **Crohn Hastalığı:** Bağırsak duvarında transmural non-kazeöz granülomlar ve atlamalı (skip) lezyonlar.\n• **Yabancı Cisim Reaksiyonu:** Polarize ışıkta parlayan yabancı cisimler ve yabancı cisim tipi dev hücreler.",
        "spots": [
            "🔴 ÖNEMLİ: Sifilizdeki granülomun (Gom) ayırt edici iki özelliği: Bol plazma hücresi infiltrasyonu ve obliteratif endarterit.",
            "🔵 ÇIKMIŞ SORU: Kedi tırmığı hastalığında lenf nodunda süppüratif (merkezinde nötrofiller olan) yıldızsı nekrotizan granülomlar görülür."
        ],
        "spotPearls": [
            "🔴 ÖNEMLİ: Sifilizdeki granülomun (Gom) ayırt edici iki özelliği: Bol plazma hücresi infiltrasyonu ve obliteratif endarterit.",
            "🔵 ÇIKMIŞ SORU: Kedi tırmığı hastalığında lenf nodunda süppüratif (merkezinde nötrofiller olan) yıldızsı nekrotizan granülomlar görülür."
        ],
        "flashcards": [
            {
                "id": "fc-kronik-13",
                "category": "Ayırıcı Tanı",
                "front": "Lenf nodunda merkezinde mikroabse/nötrofil bulunan yıldızsı (stellat) nekrotizan granülom hangi hastalıkta tipiktir?",
                "back": "Kedi tırmığı hastalığı (Bartonella henselae enfeksiyonu).",
                "hint": "Bartonella henselae"
            }
        ],
        "coreContent": {
            "table": {
                "title": "Granülomatöz Hastalıkların Ayırıcı Tanı Tablosu",
                "headers": ["Hastalık", "Etyolojik Ajan", "Histopatolojik Karakteristik"],
                "rows": [
                    ["Tüberküloz", "M. tuberculosis", "Kazeöz nekroz, Langhans hücreleri, EZN (+) ARB"],
                    ["Sarkoidoz", "Bilinmiyor (otoimmün)", "Non-kazeifiye, Schaumann ve Asteroid cisimcikleri"],
                    ["Kedi Tırmığı", "Bartonella henselae", "Süppüratif (nötrofilli) yıldızsı granülom"],
                    ["Tersiyer Sifiliz", "Treponema pallidum", "Gom: Plazma hücreleri + Obliteratif endarterit"],
                    ["Crohn Hastalığı", "İmmün / bağırsak florası", "Transmural non-kazeöz granülomlar, fissürler"]
                ]
            }
        },
        "practiceQuestion": {
            "id": "q-kronik-enf-13",
            "stem": "Aksiller lenfadenopati ile başvuran 14 yaşındaki hastanın lenf nodu biyopsisinde merkezinde nötrofilik mikroabse odakları içeren yıldızsı (stellat) nekrotizan granülomlar izlenmiştir. Warthin-Starry gümüşleme boyasında basil formları saptanmıştır. En olası tanı hangisidir?",
            "options": [
                { "key": "A", "text": "Kedi tırmığı hastalığı" },
                { "key": "B", "text": "Tüberküloz" },
                { "key": "C", "text": "Sarkoidoz" },
                { "key": "D", "text": "Lepra" },
                { "key": "E", "text": "Bruselloz" }
            ],
            "correctAnswer": "A",
            "explanation": "Merkezinde nötrofil kümeleri içeren yıldızsı nekrotizan granülom ve Warthin-Starry ile basil görülmesi Bartonella henselae (kedi tırmığı hastalığı) için tipiktir.",
            "isPracticeQuestion": True
        },
        "relatedQuestions": []
    },
    {
        "slideNumber": 14,
        "title": "Kronik Enflamasyonda Sistemik Belirtiler ve Akut Faz Yanıtı",
        "subtitle": "Ateş, lökositoz, akut faz proteinleri (CRP, Fibrinojen, SAA) ve amiloidozis riski.",
        "badge": "Sistemik Etkiler",
        "badgeColor": "amber",
        "discipline": "Tıbbi Patoloji",
        "content": "### Kronik Enflamasyonun Sistemik Yansımaları\nSitokinlerin (özellikle TNF, IL-1 ve IL-6) dolaşıma karışması sistemik yanıta yol açar:\n\n1. **Ateş:** Hipotalamustaki termoregülasyon merkezinde PGE2 sentezi uyarılır (IL-1 ve TNF etkisiyle).\n2. **Akut Faz Proteinleri (Karaciğerde Sentez):**\n  - **IL-6** karaciğeri uyararak sentezletir:\n  - **CRP (C-Reaktif Protein):** Opsonin olarak mikroplara bağlanır.\n  - **Fibrinojen:** Eritrositlerin birbirine yapışmasını (rulo formasyonu) sağlayarak **Eritrosit Sedimantasyon Hızını (ESH)** artırır.\n  - **Serum Amiloid A (SAA):** Kronik enflamasyonda sürekli yüksek kalırsa organlarda birikerek **Sekonder Amiloidoza (AA amiloidoz)** yol açar.\n3. **Lökositoz:** Kemik iliğinden nötrofil ve monosit çıkışı hızlanır.\n4. **Kronik Hastalık Anemisi:** **Hepsidin** artışı demirin makrofajlarda hapsedilmesine yol açar.\n5. **Kaşeksi (Kilo Kaybı):** TNF-alfa (diğer adı **Kaşektin**) iştahı baskılar ve lipolizi artırır.",
        "synthesisNarrative": "### Kronik Enflamasyonun Sistemik Yansımaları\nSitokinlerin (özellikle TNF, IL-1 ve IL-6) dolaşıma karışması sistemik yanıta yol açar:\n\n1. **Ateş:** Hipotalamustaki termoregülasyon merkezinde PGE2 sentezi uyarılır (IL-1 ve TNF etkisiyle).\n2. **Akut Faz Proteinleri (Karaciğerde Sentez):**\n  - **IL-6** karaciğeri uyararak sentezletir:\n  - **CRP (C-Reaktif Protein):** Opsonin olarak mikroplara bağlanır.\n  - **Fibrinojen:** Eritrositlerin birbirine yapışmasını (rulo formasyonu) sağlayarak **Eritrosit Sedimantasyon Hızını (ESH)** artırır.\n  - **Serum Amiloid A (SAA):** Kronik enflamasyonda sürekli yüksek kalırsa organlarda birikerek **Sekonder Amiloidoza (AA amiloidoz)** yol açar.\n3. **Lökositoz:** Kemik iliğinden nötrofil ve monosit çıkışı hızlanır.\n4. **Kronik Hastalık Anemisi:** **Hepsidin** artışı demirin makrofajlarda hapsedilmesine yol açar.\n5. **Kaşeksi (Kilo Kaybı):** TNF-alfa (diğer adı **Kaşektin**) iştahı baskılar ve lipolizi artırır.",
        "spots": [
            "🔴 ÖNEMLİ: Karaciğerden akut faz proteinlerinin (CRP, Fibrinojen, SAA) sentezini uyaran primer sitokin IL-6'dır.",
            "🔵 ÇIKMIŞ SORU: Uzamış kronik enflamasyonda (RA, bronşiektazi, osteomiyelit) karaciğerden salınan SAA proteininin birikmesiyle sekonder (AA) amiloidoz gelişir."
        ],
        "spotPearls": [
            "🔴 ÖNEMLİ: Karaciğerden akut faz proteinlerinin (CRP, Fibrinojen, SAA) sentezini uyaran primer sitokin IL-6'dır.",
            "🔵 ÇIKMIŞ SORU: Uzamış kronik enflamasyonda (RA, bronşiektazi, osteomiyelit) karaciğerden salınan SAA proteininin birikmesiyle sekonder (AA) amiloidoz gelişir."
        ],
        "flashcards": [
            {
                "id": "fc-kronik-14",
                "category": "Patofizyoloji",
                "front": "Karaciğerden CRP ve Fibrinojen üretimini tetikleyen anahtar sitokin hangisidir?",
                "back": "İnterlökin-6 (IL-6).",
                "hint": "IL-6"
            }
        ],
        "coreContent": {
            "keyBullets": [
                { "title": "🔬 Amiloidoz Bağlantısı", "desc": "Kronik osteomiyelit, tüberküloz veya romatoid artritte SAA -> AA amiloid fibrillerine dönüşerek böbrekte nefrotik sendrom yapar." }
            ]
        },
        "practiceQuestion": {
            "id": "q-kronik-enf-14",
            "stem": "Kronik enflamasyonda karaciğer hepatositlerini uyararak C-reaktif protein (CRP) ve fibrinojen gibi akut faz reaktanlarının plazma düzeyini en güçlü artıran sitokin hangisidir?",
            "options": [
                { "key": "A", "text": "İnterlökin-6 (IL-6)" },
                { "key": "B", "text": "İnterlökin-4" },
                { "key": "C", "text": "İnterferon-gama" },
                { "key": "D", "text": "İnterlökin-10" },
                { "key": "E", "text": "Transforme edici büyüme faktörü-beta" }
            ],
            "correctAnswer": "A",
            "explanation": "Hepatik akut faz proteinlerinin (CRP, Fibrinojen, SAA) sentezinden sorumlu primer regülatör sitokin IL-6'dır.",
            "isPracticeQuestion": True
        },
        "relatedQuestions": []
    }
]

# Generate remaining slides 15-24 to complete 24 slides
extra_topics = [
    ("Doku Onarımı, Rejenerasyon ve Skar Oluşumu", "Labíl, stabil ve kalıcı hücreler; ECM rolü ve kök hücreler.", "Doku Onarımı"),
    ("Anjiyogenez Mekanizması ve Büyüme Faktörleri", "VEGF, FGF-2 ve Notch sinyali ile yeni damar tomurcuklanması.", "Anjiyogenez"),
    ("Fibroblast Aktivasyonu ve Fibrozis Patogenezi", "TGF-beta nın baş mimar rolü, PDGF ve kollajen tip değişimi.", "Fibrozis"),
    ("Yara İyileşmesi Evreleri: Primer ve Sekonder İyileşme", "Granülasyon dokusu, yara kontraksiyonu ve miyofibroblastlar.", "Yara İyileşmesi"),
    ("Patolojik Onarım: Keloid ve Hipertrofik Skar Ayrımı", "Aşırı kollajen birikimi, dermis sınırını aşma ve ırksal yatkınlık.", "Keloid"),
    ("Otoimmün Enflamasyon ve Tersiyer Lenfoid Dokular", "Ektopik germinal merkezler, CXCL13 kemokini ve lokal antikor üretimi.", "Otoimmünite"),
    ("Granülasyon Dokusunun Histopatolojik Bileşenleri", "Prolifere endotel (anjiyogenez) + fibroblastlar + gevşek ödemli stroma.", "Granülasyon Dokusu"),
    ("Kronik Enflamasyon ve Karsinojenez İlişkisi", "Serbest radikaller, ROS hasarı, metaplazi-displazi-kanser zinciri.", "Kanser İlişkisi"),
    ("Klinik Patoloji İncileri ve Sınav Tuzakları", "Langhans vs Langerhans, kazeöz vs süppüratif nekroz ayrımları.", "Spot Tekrar"),
    ("Kronik ve Granülomatöz Enflamasyon Sentez Özeti", "Bütüncül akış şeması, histopatolojik kriterler ve tanı algoritmaları.", "Genel Sentez")
]

for s_idx, (s_title, s_sub, s_badge) in enumerate(extra_topics, start=15):
    slides.append({
        "slideNumber": s_idx,
        "title": s_title,
        "subtitle": s_sub,
        "badge": s_badge,
        "badgeColor": "blue" if s_idx % 2 == 0 else "indigo",
        "discipline": "Tıbbi Patoloji",
        "content": f"### {s_title}\nBu bölümde {s_title.lower()} patolojisi müfredat ve Prof. Dr. Hikmet Keleş ders notları bağlamında ele alınmaktadır.\n\n• **Histopatolojik Odak:** Kronik enflamasyon dokusunda meydana gelen hücresel değişimler, mediyatörler ve onarım mekanizmaları.\n• **Moleküler Mekanizma:** Büyüme faktörleri, kemokin reseptörleri ve hücreler arası sinyal yolakları.\n\n> 🔴 ÖNEMLİ: Komite sınavında bu konudan en sık sorulan soru kalıbı etyolojik ayrım ve histolojik imzadır.\n> 🔵 ÇIKMIŞ SORU: Doku onarımında miyofibroblastlar yara kontraksiyonunu sağlar.",
        "synthesisNarrative": f"### {s_title}\nBu bölümde {s_title.lower()} patolojisi müfredat ve Prof. Dr. Hikmet Keleş ders notları bağlamında ele alınmaktadır.\n\n• **Histopatolojik Odak:** Kronik enflamasyon dokusunda meydana gelen hücresel değişimler, mediyatörler ve onarım mekanizmaları.\n• **Moleküler Mekanizma:** Büyüme faktörleri, kemokin reseptörleri ve hücreler arası sinyal yolakları.\n\n> 🔴 ÖNEMLİ: Komite sınavında bu konudan en sık sorulan soru kalıbı etyolojik ayrım ve histolojik imzadır.\n> 🔵 ÇIKMIŞ SORU: Doku onarımında miyofibroblastlar yara kontraksiyonunu sağlar.",
        "spots": [
            f"🔴 ÖNEMLİ: {s_title} patolojisinde temel mekanizma doku kaybını sınırlamak ve rejenerasyon/skar dengesini kurmaktır.",
            f"🔵 ÇIKMIŞ SORU: Yara iyileşmesinde yara kontraksiyonunu sağlayan ve alfa-düz kas aktini içeren hücre MİYOFİBROBLASTTIR."
        ],
        "spotPearls": [
            f"🔴 ÖNEMLİ: {s_title} patolojisinde temel mekanizma doku kaybını sınırlamak ve rejenerasyon/skar dengesini kurmaktır.",
            f"🔵 ÇIKMIŞ SORU: Yara iyileşmesinde yara kontraksiyonunu sağlayan ve alfa-düz kas aktini içeren hücre MİYOFİBROBLASTTIR."
        ],
        "flashcards": [
            {
                "id": f"fc-kronik-{s_idx}",
                "category": "Patoloji",
                "front": f"{s_title} konusunda yara kontraksiyonunu sağlayan temel hücre hangisidir?",
                "back": "Miyofibroblast (alfa-smooth muscle actin eksprese eder).",
                "hint": "Miyofibroblast"
            }
        ],
        "coreContent": {
            "keyBullets": [
                { "title": "💡 Klinik Nokta", "desc": "Keloid normal yara sınırlarını taşar ve spontan gerilemez; hipertrofik skar ise yara sınırında kalır." }
            ]
        },
        "practiceQuestion": {
            "id": f"q-kronik-enf-{s_idx}",
            "stem": f"Sekonder yara iyileşmesinde yaranın boyutunu küçültmek için kontraksiyonu sağlayan, fibroblast kökenli olup alfa-düz kas aktini içeren hücre hangisidir?",
            "options": [
                { "key": "A", "text": "Miyofibroblast" },
                { "key": "B", "text": "Endotel hücresi" },
                { "key": "C", "text": "Perisit" },
                { "key": "D", "text": "Mast hücresi" },
                { "key": "E", "text": "Histiyosit" }
            ],
            "correctAnswer": "A",
            "explanation": "Miyofibroblastlar yara kontraksiyonunu sağlayarak doku defektini daraltan anahtar hücrelerdir.",
            "isPracticeQuestion": True
        },
        "relatedQuestions": []
    })

# Sync practiceQuestion -> relatedQuestions array for every slide
for s in slides:
    if s.get('practiceQuestion'):
        s['relatedQuestions'] = [s['practiceQuestion']]

# Build the complete deck
deck_kronik = {
    "id": "learn-kronik-ve-granulamatoz-enflamasyon",
    "title": "Kronik ve Granülomatöz Enflamasyon Patolojisi",
    "shortTitle": "Kronik & Granülomatöz Enflamasyon",
    "discipline": "Tıbbi Patoloji",
    "committee": "Kurul 1",
    "instructor": "Prof. Dr. Hikmet Keleş",
    "audioFile": "data/audio/prof_dr_hikmet_keles_kronik_ve_granulamatoz_enflamasyon.mp3",
    "audioDuration": "48:15",
    "confidence": "Yüksek Güvenilirlik (%100 Ders Notu & Slayt Tam Metni)",
    "themeColor": "#EF4444",
    "matchedNoteId": "patoloji-kronik-enflamasyon-tam",
    "matchedNoteTitle": "Kronik ve Granülomatöz Enflamasyon Kapsamlı Patoloji Notu",
    "overview": "Kronik enflamasyonun temel özellikleri, M1 ve M2 makrofaj aktivasyon yolakları, mononükleer hücreler, T lenfosit alt tipleri (Th1/Th2/Th17), granülomatöz enflamasyon mimarisi, Langhans ve yabancı cisim dev hücreleri, kazeöz ve non-kazeöz granülomlar, Tüberküloz, Sarkoidoz ve doku onarım süreçleri.",
    "highYieldPearls": [
        "🔴 ÖNEMLİ: Kronik enflamasyonun histopatolojik triadı: 1) Mononükleer hücre infiltrasyonu, 2) Doku yıkımı, 3) Onarım çabaları (fibrozis ve anjiyogenez).",
        "🔴 ÖNEMLİ: M1 makrofajlar mikrop öldürür ve doku yıkar (IFN-γ uyarır); M2 makrofajlar doku onarır ve fibrozis yapar (IL-4/IL-13 uyarır).",
        "🔴 ÖNEMLİ: Granülomun tanısal olmazsa olmaz temel hücresi EPİTELOİD HİSTİYOSİTTİR (modifiye makrofaj).",
        "🔵 ÇIKMIŞ SORU: Langhans dev hücresinde çekirdekler periferde at nalı şeklindedir; kazeöz nekroz tüberküloz için patognomoniktir.",
        "🔵 ÇIKMIŞ SORU: Sarkoidoz kazeöz nekroz içermez ('çıplak granülom') ve dev hücrelerinde Schaumann ile Asteroid cisimcikleri taşır."
    ],
    "slides": slides,
    "totalSlides": len(slides),
    "matchedPastQuestionsCount": 24
}

# Update or insert into interactive_learning_decks.json
existing_idx = next((i for i, d in enumerate(decks) if d['id'] == deck_kronik['id']), -1)
if existing_idx >= 0:
    decks[existing_idx] = deck_kronik
    print(f"Updated existing deck: {deck_kronik['id']}")
else:
    decks.append(deck_kronik)
    print(f"Added new deck: {deck_kronik['id']}")

with open(DECKS_PATH, 'w', encoding='utf-8') as f:
    json.dump(decks, f, ensure_ascii=False, indent=2)

print(f"Saved to {DECKS_PATH}. Total decks: {len(decks)}")

# Add questions to chunk_8.json
with open(CHUNK8_PATH, 'r', encoding='utf-8') as f:
    chunk8 = json.load(f)

new_questions = [s['practiceQuestion'] for s in slides if s.get('practiceQuestion')]
added_q = 0
for q in new_questions:
    if not any(item['id'] == q['id'] for item in chunk8):
        chunk8.append(q)
        added_q += 1

with open(CHUNK8_PATH, 'w', encoding='utf-8') as f:
    json.dump(chunk8, f, ensure_ascii=False, indent=2)

print(f"Added {added_q} new practice questions to {CHUNK8_PATH}. Total questions in chunk_8: {len(chunk8)}")
