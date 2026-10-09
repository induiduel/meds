# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_5_slides():
    slides = []

    # Slide 41
    slides.append({
        "id": "k1-15-s41",
        "title": "Anjiyogenez: Mevcut Damarlardan Yeni Damar Oluşumu",
        "content": "Yeni oluşan dokunun oksijen ve besin ihtiyacını karşılamak için damarlanma şarttır:\n\n- **İki Farklı Damar Oluşum Mekanizması (Sınav Spotu):**\n  1. **Vaskülogenez (Vaskülogenizis):** Embriyonik gelişim sırasında primitif endotelyal öncül hücrelerin (anjiyoblastlar / endotel progenitörleri) sıfırdan bir araya gelerek ilk damar ağını (pleksus) kurmasıdır.\n  2. **Anjiyogenez (Neovaskülarizasyon):** Erişkin organizmada doku onarımı, menstrüel siklus veya tümör büyümesi sırasında **önceden var olan mevcut olgun damarlardan yeni damar dallarının tomurcuklanmasıdır**.\n- **Kritik Biyolojik Görev:** Anjiyogenez olmadan doku onarımı imkansızdır; çünkü çoğalan fibroblastların ve epitel hücrelerinin ihtiyaç duyduğu oksijen ve yapıtaşları ancak bu yeni kapillerler yoluyla taşınır.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Vaskülogenez vs Anjiyogenez",
                "Vaskülogenez (Embriyogenez)",
                "Kemik iliği/mezoderm kökenli anjiyoblastlardan sıfırdan primer vasküler pleksus oluşturulmasıdır.",
                "Anjiyogenez (Yara Onarımı / Erişkin)",
                "Mevcut komşu kılcal damarlardan tomurcuklanarak (sprouting) yara içine yeni dallar uzatılmasıdır."
            ),
            make_cloze(
                "Önceden var olan mevcut damarlardan yeni damar tomurcuklanması sürecine anjiyogenez denir.",
                "anjiyogenez",
                "Yeni kapiller tomurcuklanması terimi"
            )
        ]
    })

    # Slide 42
    slides.append({
        "id": "k1-15-s42",
        "title": "Anjiyogenezin 1. ve 2. Basamakları: Vazodilatasyon ve Perisit Ayrılması",
        "content": "Bir damarın yeni bir dal verebilmesi için önce mevcut yapısını gevşetmesi gerekir (Sınav Spotu):\n\n- **1. Basamak: Vazodilatasyon ve Geçirgenlik Artışı:**\n  - Hipoksik yara dokusundan salınan mediyatörlerin etkisiyle ana damarda **Nitrik Oksit (NO)** üretilir; damar genişler (vazodilatasyon).\n  - **VEGF (Vasküler Endotel Büyüme Faktörü)** etkisiyle endotel hücreleri arasındaki bağlantılar gevşer, vasküler geçirgenlik tavan yapar.\n- **2. Basamak: Perisitlerin Ayrılması (Pericyte Detachment):**\n  - Normalde olgun kapillerlerin dış yüzeyini bir kılıf gibi saran ve damarı stabilize eden destek hücrelerine **perisitler** denir.\n  - Tomurcuklanmanın başlayabilmesi için perisitlerin damar duvarından ayrılması zorunludur.\n  - Bu ayrılmayı **Angiopoietin-2 (Ang-2)** molekülü sağlar; Ang-2, endoteldeki Tie-2 reseptörünü bloke ederek perisit tutunmasını çözer.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Anjiyogenezin Başlangıç Gevşeme Zinciri",
                [
                    "1. Hipoksi ve İskemi: Yara merkezinde oksijen düşer ve HIF-1alfa faktörü açılır.",
                    "2. VEGF ve NO Salınımı: Ana damarda endotelyal NO ile vazodilatasyon gerçekleşir.",
                    "3. Geçirgenlik Artışı: Plazma proteinleri dokuya sızarak geçici matriksi destekler.",
                    "4. Ang-2 Sinyali: Angiopoietin-2, perisitlerin damar dış yüzeyinden ayrılmasını tetikler.",
                    "5. Serbestleşen Endotel: Endotel hücreleri bazal membranı eriterek göçe hazır hale gelir."
                ]
            ),
            make_quiz(
                "Anjiyogenezin erken aşamasında ana damarın vazodilatasyonunu sağlayan temel mediyatör ile perisitlerin damar duvarından ayrılmasını tetikleyen molekül ikilisi hangisidir?",
                [
                    {"key": "A", "text": "Nitrik Oksit (NO) ve Angiopoietin-2 (Ang-2)", "isCorrect": True, "explanation": "Doğru cevap A'dır: NO vazodilatasyonu sağlar; Ang-2 ise perisitlerin gevşeyip damardan ayrılmasını tetikler."},
                    {"key": "B", "text": "Kalsitonin ve Parathormon", "isCorrect": False, "explanation": "Kemik ve kalsiyum regülasyonu hormonlarıdır."},
                    {"key": "C", "text": "Gastrin ve Sekretin", "isCorrect": False, "explanation": "Mide-bağırsak hormonlarıdır."},
                    {"key": "D", "text": "Lökotrien B4 ve Trombin", "isCorrect": False, "explanation": "Enflamasyon ve koagülasyon faktörleridir."}
                ]
            )
        ]
    })

    # Slide 43
    slides.append({
        "id": "k1-15-s43",
        "title": "Anjiyogenezin 3. ve 4. Basamakları: ECM Yıkımı ve Tip Hücresi Göçü",
        "content": "Perisitler ayrıldıktan sonra endotelin önündeki fiziksel bariyerlerin temizlenmesi gerekir:\n\n- **3. Basamak: Bazal Membran ve ECM'nin Proteolitik Yıkımı:**\n  - Endotel hücreleri **Matriks Metalloproteinazlar (MMP'ler)** ve plazminojen aktivatörleri salgılar.\n  - Bu enzimler damarın kendi bazal membranını (Tip IV kollajen) ve komşu interstisyel matriksi eriterek endotelin çıkabileceği bir delik açar.\n- **4. Basamak: Endotel Göçü ve Tip Hücresi (Tip Cell):**\n  - Yeni tomurcuğun en önünde liderlik eden özelleşmiş endotel hücresine **Uç Hücresi (Tip Cell)** denir.\n  - Tip hücresi mitoz yapmaz! Uzun sitoplazmik uzantılarıyla (**filopodia**) yara dokusundan gelen VEGF gradyanını koklar ve en yüksek oksijensiz alana doğru sürünür.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Uç Hücresi (Tip Cell) vs Gövde Hücresi (Stalk Cell)",
                "Uç Hücresi / Tip Cell (Öncü Lider)",
                "Filopodiaları ile VEGF gradyanını algılar, yönü belirler ve göç eder; bölünme yeteneği düşüktür.",
                "Gövde Hücresi / Stalk Cell (İnşaatçı Takipçi)",
                "Tip hücresinin arkasından gelir; hızla prolifere olur ve damarın içi boş lümenini inşa eder."
            ),
            make_cloze(
                "Anjiyogenik tomurcuğun en ucunda filopodiaları ile VEGF gradyanına doğru göç eden öncü endotel hücresine tip hücresi denir.",
                "tip",
                "Tomurcuğun en ucundaki kılavuz hücre sıfatı"
            )
        ]
    })

    # Slide 44
    slides.append({
        "id": "k1-15-s44",
        "title": "Notch Sinyali ve Dll4: Anjiyogenik Kaosu Önleme",
        "content": "Anjiyogenez sırasında her endotel hücresi aynı anda 'uç hücresi' olmaya kalkarsa ne olur? Damar kör bir yumağa döner ve lümen oluşamaz:\n\n- **Lateral İnhibisyon Mekanizması (Sınav Spotu):**\n  - En yüksek VEGF alan endotel hücresi öncü **Tip hücresi** haline gelir.\n  - Tip hücresi, yüzeyinde **Delta-like ligand 4 (Dll4)** ekspresyonunu artırır.\n  - Dll4, arkasındaki komşu endotel hücrelerinin üzerindeki **Notch-1** reseptörüne bağlanır.\n- **Sonuç:**\n  - Notch sinyali alan arkadaki hücrelerde VEGF reseptörleri (VEGFR-2) baskılanır.\n  - Bu hücrelerin de tip hücresi olması engellenir; onlar birer **Gövde Hücresi (Stalk Cell)** haline gelir.\n  - Stalk hücreleri göç etmez, çoğalarak damarın tübüler boru yapısını uzatır.\n- **Klinik Önemi:** Anti-Dll4 ilaçlar verildiğinde aşırı ama işlevsiz kör damar yumakları oluşur.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Notch-Dll4 Lateral İnhibisyon Döngüsü",
                [
                    "1. Yüksek VEGF Uyarısı: En öndeki endotel hücresi Tip hücresi olarak seçilir.",
                    "2. Dll4 Ekspresyonu: Tip hücresi zarına bol miktarda Dll4 ligandı yerleştirir.",
                    "3. Notch Reseptör Aktivasyonu: Arkadaki komşu hücrelerde Notch yolu aktive edilir.",
                    "4. VEGFR-2 Baskılanması: Arkadaki hücrelerin yeni tomurcuk çıkarması engellenir.",
                    "5. Stalk Hücresi Olma: Arkadaki hücreler bölünerek damar lümenini ve boru gövdesini oluşturur."
                ]
            ),
            make_quiz(
                "Anjiyogenezde öncü uç hücresinin (tip cell) arkasındaki endotel hücrelerinin kontrolsüz tomurcuklanmasını engelleyip onları tüp oluşturan gövde hücrelerine (stalk cell) dönüştüren moleküler sinyal yolağı hangisidir?",
                [
                    {"key": "A", "text": "Wnt / beta-katenin", "isCorrect": False, "explanation": "Wnt kök hücre nişinde ve embriyogenezde etkilidir."},
                    {"key": "B", "text": "Notch ve Dll4 (Delta-like ligand 4)", "isCorrect": True, "explanation": "Doğru cevap B'dir: Notch/Dll4 yolağı lateral inhibisyon ile tip hücresi arkasındaki endoteli stalk hücresine dönüştürür."},
                    {"key": "C", "text": "JAK / STAT", "isCorrect": False, "explanation": "Sitokin sinyal yolağıdır."},
                    {"key": "D", "text": "Fas / FasL", "isCorrect": False, "explanation": "Apoptoz ölüm yolağıdır."}
                ]
            )
        ]
    })

    # Slide 45
    slides.append({
        "id": "k1-15-s45",
        "title": "Anjiyogenezin 5, 6 ve 7. Basamakları: Lümenleşme ve Damar Olgunlaşması",
        "content": "Tomurcuk uzadıktan sonra gerçek bir fonksiyonel kan kanalına dönüşmesi gerekir:\n\n- **5. Basamak: Tübüler Lümen Oluşumu (Vakuolizasyon):**\n  - Stalk endotel hücreleri içinde intrasellüler pinositik vakuoller birleşir.\n  - İki komşu endotel hücresi arasında içi boş tübüler bir lümen açılır.\n- **6. Basamak: Karşı Tomurcukla Birleşme (Anastomoz):**\n  - Karşı yönden gelen başka bir kapiller ilmeğiyle uç uca birleşerek kapalı bir dolaşım döngüsü kurulur; kan akımı başlar.\n- **7. Basamak: Damar Olgunlaşması ve Stabilizasyon (Sınav Spotu):**\n  - Kan akımı başladığında damarın sızdırmaz hale getirilmesi şarttır.\n  - Endotel hücreleri **PDGF** salgılayarak çevre dokudaki perisitleri ve düz kas hücrelerini damar duvarına çağırır.\n  - **Angiopoietin-1 (Ang-1)**, endoteldeki **Tie-2** reseptörüne bağlanarak perisitlerin endotelle sıkı bağ kurmasını sağlar.\n  - **TGF-β**, endotel proliferasyonunu durdurur ve yeni bazal membran (kollajen Tip IV ve laminin) sentezini uyarır.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Aşama", "Sorumlu Molekül", "Hücresel Yanıt", "Nihai Vasküler Sonuç"],
                [
                    ["Perisit Çağırma", "PDGF", "Perisitler damara göç eder", "Damar dış duvarının sarılması"],
                    ["Damar Stabilizasyonu", "Angiopoietin-1 (Tie-2)", "Perisit-endotel sıkı bağlantısı", "Sızdırmaz ve kalıcı damar yapısı"],
                    ["Mitozu Durdurma", "TGF-beta", "Endotel bölünmesi durur", "Olgun bazal membran sentezi"]
                ]
            ),
            make_cloze(
                "Yeni oluşan kapillerlerin perisitlerle sarılarak stabilize edilmesini sağlayan temel büyüme faktörü PDGF ve Angiopoietin-1 molekülüdür.",
                "Angiopoietin-1",
                "Tie-2 reseptörüne bağlanan damar olgunlaştırıcı faktör"
            )
        ]
    })

    # Slide 46
    slides.append({
        "id": "k1-15-s46",
        "title": "VEGF Ailesi ve Anjiyogenik Reseptörler",
        "content": "Anjiyogenezin en tartışmasız baş aktörü **Vasküler Endotel Büyüme Faktörü (VEGF)** ailesidir:\n\n- **Ailenin Üyeleri:** VEGF-A, VEGF-B, VEGF-C, VEGF-D ve PIGF (Plasental Büyüme Faktörü).\n- **VEGF-A (Klasik VEGF - Sınav Spotu):**\n  - Anjiyogenezin ana tetikleyicisidir. Mezenkimal hücreler, makrofajlar ve tümör hücreleri tarafından hipoksiye yanıt olarak salgılanır.\n  - Hipoksi anında hücrede **HIF-1α (Hipoksi İle İndüklenen Faktör-1α)** parçalanmaktan kurtulur, çekirdeğe girer ve devasa bir VEGF-A transkripsiyonu başlatır.\n- **Reseptörler:**\n  - **VEGFR-2 (KDR/Flk-1):** Endotel üzerindeki **en önemli fonksiyonel reseptördür**; endotel mitozunu, göçünü ve anjiyogenezi neredeyse tamamen bu reseptör yürütür.\n  - **VEGFR-1 (Flt-1):** VEGF'e çok yüksek afiniteyle bağlanır ancak sinyali zayıftır; genellikle bir 'tuzak/yem reseptör' (decoy receptor) gibi davranarak anjiyogenezi dengeler.\n  - **VEGFR-3:** Kan damarlarında değil, **Lenfanjiogenezde (lenf damarlarının oluşumunda)** rol oynar (VEGF-C ve VEGF-D ile uyarılır).",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "VEGFR-2 vs VEGFR-3 Reseptör Fonksiyonu",
                "VEGFR-2 (Kan Damarı Anjiyogenezi)",
                "VEGF-A ile uyarılır; kılcal kan damarlarının tomurcuklanmasını, endotel mitozunu ve göçünü yönetir.",
                "VEGFR-3 (Lenf Damarı Lenfanjiogenezi)",
                "VEGF-C ve VEGF-D ile uyarılır; lenf damarlarının tomurcuklanmasını ve lenfatik drenajı sağlar."
            ),
            make_quiz(
                "Anjiyogenezde endotel hücrelerinin proliferasyonunu, göçünü ve damar tomurcuklanmasını yöneten en önemli fonksiyonel reseptör tirozin kinaz hangisidir?",
                [
                    {"key": "A", "text": "VEGFR-1 (Flt-1)", "isCorrect": False, "explanation": "VEGFR-1 daha çok düzenleyici/tuzak reseptördür."},
                    {"key": "B", "text": "VEGFR-2 (Flk-1 / KDR)", "isCorrect": True, "explanation": "Doğru cevap B'dir: Endotel hücresinde anjiyogenezin tüm klasik mitojenik ve göç sinyallerini ileten ana reseptör VEGFR-2'dir."},
                    {"key": "C", "text": "VEGFR-3", "isCorrect": False, "explanation": "VEGFR-3 lenfanjiogenezden sorumludur."},
                    {"key": "D", "text": "İnsülin Reseptörü", "isCorrect": False, "explanation": "Glikoz metabolizması reseptörüdür."}
                ]
            )
        ]
    })

    # Slide 47
    slides.append({
        "id": "k1-15-s47",
        "title": "FGF, PDGF ve Angiopoietinlerin Orkestrasyonu",
        "content": "Anjiyogenez tek bir enstrümanın değil, tam bir biyokimyasal orkestranın eseridir:\n\n- **FGF-2 (Temel Fibroblast Büyüme Faktörü - bFGF - Sınav Spotu):**\n  - Endotel hücre göçünü uyarır.\n  - Yara tabanında epitel hücrelerinin ve fibroblastların çoğalmasını da eşzamanlı tetikleyerek doku dolgusunu hızlandırır.\n- **Angiopoietin-1 (Ang-1) vs Angiopoietin-2 (Ang-2) Dengesi:**\n  - **Ang-1:** Endotel hücresindeki **Tie-2** reseptörüne bağlanarak perisitleri çağırır ve damarı **stabilize eder (kapatır/olgunlaştırır)**.\n  - **Ang-2:** Tie-2 reseptörünü yarışmalı olarak bloke eder; perisitleri uzaklaştırarak damarı **gevşetir ve yeni tomurcuklanmaya açar**.\n- **PDGF (Trombosit Kaynaklı Büyüme Faktörü):** Düz kas hücrelerini ve perisitleri yeni tomurcuğun etrafına çekerek damarın elastik duvarını örer.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Molekül Adı", "Hedef Reseptör", "Anjiyogenezdeki Net Etkisi"],
                [
                    ["VEGF-A", "VEGFR-2", "Damar tomurcuklanması, endotel mitozu ve yüksek geçirgenlik"],
                    ["Ang-2", "Tie-2 antagonisti", "Perisitleri ayırma, damarı anjiyogeneze gevşetme"],
                    ["FGF-2 (bFGF)", "FGFR", "Endotel göçü ve fibroblast proliferasyonu"],
                    ["Ang-1", "Tie-2 agonisti", "Perisit tutunması, damar matürasyonu ve sızdırmazlık"],
                    ["PDGF", "PDGFR-beta", "Perisit ve düz kas hücresi toplanması"]
                ]
            ),
            make_cloze(
                "Damar olgunlaşmasında perisitlerin endotel üzerine tutunmasını sağlayan molekül Angiopoietin-1 iken, perisitleri ayıran zıt molekül Angiopoietin-2'dir.",
                "Angiopoietin-2'dir",
                "Damarı gevşetip tomurcuklanmaya açan Tie-2 antagonisti faktör"
            )
        ]
    })

    # Slide 48
    slides.append({
        "id": "k1-15-s48",
        "title": "Anjiyogenezin Tıptaki İki Yüzü: Onarım vs Tümör Biyolojisi",
        "content": "Anjiyogenez, yara iyileşmesinde hayat kurtaran bir dostken; onkolojide kanserin yayılmasını sağlayan ölümcül bir düşmana dönüşür:\n\n- **Doku Onarımında Anjiyogenez (Fizyolojik):**\n  - Düzenli, kontrollü, basamaklı ve sonlanan bir süreçtir.\n  - İyileşme tamamlandığında damarlar olgunlaşır, fazla kılcallar apoptozla geriler (avasküler skar kalır).\n- **Kanserde Anjiyogenez (Patolojik):**\n  - 1-2 mm çapını aşan tümörler oksijensiz kalır; aşırı kontrolsüz VEGF salgılarlar.\n  - Tümör damarları son derece kaotik, kıvrımlı, kör sonlanan ve aşırı geçirgendir.\n- **Farmakolojik Hedef (Anti-Anjiyogenik Tedaviler):**\n  - **Bevacizumab (Anti-VEGF monoklonal antikoru):** VEGF'i nötralize ederek tümör damarlanmasını kurutur.\n  - Göz hastalıklarında (diyabetik retinopati ve yaşa bağlı makula dejenerasyonu) görmeyi kurtarmak için göze anti-VEGF enjeksiyonları yapılır.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Fizyolojik Yara Anjiyogenezi vs Patolojik Tümör Anjiyogenezi",
                "Yara Anjiyogenezi (Geçici ve Düzenli)",
                "Doku dolduğunda damarlar perisitlerle sarılır, fazla kapillerler apoptozla temizlenir; skar avaskülerleşir.",
                "Tümör Anjiyogenezi (Kaotik ve Sürekli)",
                "Hiçbir zaman olgunlaşmaz; sızdıran, düzensiz damar yumaklarıyla tümörün metastaz yapmasına yol açar."
            ),
            make_recall(
                "Yara onarımı tamamlandığında pembe ve yoğun damarlı granülasyon dokusunun beyaz/soluk renkli avasküler bir skara dönüşmesinin nedeni nedir?",
                "Artık oksijen ihtiyacı kalmadığı için yeni kılcal damarların apoptoza uğrayarak gerilemesi ve yerini yoğun sıkı kollajen liflerine bırakmasıdır."
            )
        ]
    })

    # Slide 49 - CHECKPOINT 5
    slides.append({
        "id": "k1-15-s49",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 5] Anjiyogenez Mekanizması ve Büyüme Faktörleri",
        "content": "Bu checkpointte neovaskülarizasyonun moleküler koreografisini pekiştiriyoruz:\n\n- **Vaskülogenez vs Anjiyogenez:** Vaskülogenez embriyoda sıfırdan yapım; anjiyogenez mevcut damardan tomurcuklanmadır.\n- **Sıralı Basamaklar:**\n  1. NO ile vazodilatasyon ve VEGF ile geçirgenlik artışı.\n  2. Ang-2 ile perisitlerin ayrılması.\n  3. MMP'ler ile bazal membran ve ECM'nin delinmesi.\n  4. **Tip hücresi (Uç hücresi)** önderliğinde VEGF gradyanına doğru filopodial göç.\n  5. **Notch/Dll4** lateral inhibisyonuyla arkadaki hücrelerin **Stalk hücresi (Gövde hücresi)** yapılması.\n  6. Vakuolizasyonla tübüler lümen açılması ve anastomoz.\n  7. **PDGF ve Ang-1 (Tie-2)** ile perisitlerin damarı sarması ve **TGF-β** ile bazal membran örülmesi.\n- **Reseptörler:** VEGFR-2 (kan damarı anjiyogenezi), VEGFR-3 (lenfanjiogenez).",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Anjiyogenezin 5 Temel Basamağının Özeti",
                [
                    "1. Gevşeme ve Delme: NO ile vazodilatasyon, Ang-2 ile perisit ayrılması ve MMP'lerle bazal membran delinmesi.",
                    "2. Kılavuz Göç: Tip hücresi filopodialarıyla VEGF gradyanına doğru ilerler.",
                    "3. Lateral Sınır: Dll4-Notch sinyali arkadaki stalk hücrelerini çoğaltarak lümeni uzatır.",
                    "4. Stabilizasyon: PDGF ve Ang-1 perisitleri geri çağırarak damarı kilitler, TGF-beta bazal membran örer.",
                    "5. Olgunlaşma ve Avaskülerleşme: Onarım tamamlanınca fazla damarlar apoptozla çekilir ve skar kalır."
                ]
            ),
            make_table(
                ["Faktör", "Reseptör", "Temel Görev"],
                [
                    ["VEGF-A", "VEGFR-2", "Tomurcuklanma, mitoz ve sızıntı"],
                    ["Ang-2", "Tie-2 (antagonist)", "Perisitleri ayırıp gevşetme"],
                    ["Dll4", "Notch-1", "Stalk hücresi denetimi (kaosu önleme)"],
                    ["Ang-1", "Tie-2 (agonist)", "Perisit tutunması ve olgunlaşma"],
                    ["PDGF", "PDGFR-beta", "Perisit ve düz kas hücresi göçü"]
                ]
            )
        ]
    })

    # Slide 50
    slides.append({
        "id": "k1-15-s50",
        "title": "Mini Vaka: İskemik Yara İyileşmesinde Anti-VEGF Tedavisinin Yan Etkisi",
        "content": "65 yaşında metastatik kolon kanseri nedeniyle onkoloji kliniğinde kemoterapi ve **Bevacizumab (Anti-VEGF monoklonal antikoru)** alan bir hastaya, akut apandisit nedeniyle acil laparotomi yapılıyor:\n\n- **Ameliyat Sonrası 10. Gün:** Hastanın laparotomi insizyonunun hiç kaynamadığı, yara dudaklarının soluk, avasküler ve kuru kaldığı; granülasyon dokusunun hiç gelişmediği ve dikişlerin açıldığı (yara dehisensi) saptanıyor.\n- **Patolojik Açıklama:**\n  - Bevacizumab ilacı hastanın tümör damarlarını kuruturken, yara iyileşmesi için gereken fizyolojik VEGF-A sinyalini de tamamen bloke etmiştir.\n  - Endoteldeki VEGFR-2 uyarılamadığı için endotel tomurcuklanamamış, anjiyogenez gelişmemiş ve granülasyon dokusu kurulamamıştır.\n- **Cerrahi Kural:** Elektif ameliyat planlanan kanser hastalarında anti-anjiyogenik ilaçlar (bevacizumab) ameliyattan en az 4-6 hafta önce kesilmelidir!",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_branching(
                "Klinik Karar: Kanser Hastasında Yara Açılması ve Anti-VEGF İlişkisi",
                "Hastanın yarasının kaynamaması karşısında onkoloji ve cerrahi konseyi toplanıyor. En rasyonel patolojik ve terapötik yaklaşım hangisidir?",
                [
                    {
                        "text": "'Hastaya daha yüksek doz anti-VEGF ilacı verelim, yara hemen kapanır.'",
                        "outcome": "Ölümcül hata: Anti-VEGF anjiyogenezi daha da felç eder.",
                        "isCorrect": False
                    },
                    {
                        "text": "Anti-VEGF tedavisini derhal durdurmak, yarayı enfeksiyondan koruyarak sekonder cerrahi kapatma planlamak ve damarlanmanın toparlanması için en az 4 hafta beklemek",
                        "outcome": "Kusursuz onkolojik-cerrahi karar: İlacın yarı ömrü bitince fizyolojik VEGF devreye girer ve yara iyileşir.",
                        "isCorrect": True
                    },
                    {
                        "text": "'Yara iyileşmesinde damarların hiçbir önemi yoktur, hastayı taburcu edelim.'",
                        "outcome": "Ağır cerrahi ihmal.",
                        "isCorrect": False
                    }
                ]
            ),
            make_quiz(
                "Bu vakada hastanın cerrahi yarasında granülasyon dokusunun kurulamamasının doğrudan nedeni aşağıdakilerden hangisidir?",
                [
                    {"key": "A", "text": "Anti-VEGF ilacının endotel göçünü ve anjiyogenezi bloke etmesi", "isCorrect": True, "explanation": "Doğru cevap A'dır: Bevacizumab VEGF'i bağlayarak anjiyogenezi durdurur; damarlanma olmadan granülasyon dokusu kurulamaz."},
                    {"key": "B", "text": "Hastada trombosit sayısının 1 milyonun üzerine çıkması", "isCorrect": False, "explanation": "Trombositoz yaranın açılmasına neden olmaz."},
                    {"key": "C", "text": "Karaciğerin aniden 3 kat büyümesi", "isCorrect": False, "explanation": "Konuyla ilgisi yoktur."},
                    {"key": "D", "text": "Yara kenarlarında aşırı epitel birikmesi", "isCorrect": False, "explanation": "Yara avasküler ve kurudur."}
                ]
            )
        ]
    })

    return slides
