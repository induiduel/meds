# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_10_slides():
    slides = []

    # Slide 91
    slides.append({
        "id": "k1-15-s91",
        "title": "Parankimal Organ Fibrozisi: İyileşmenin Patolojiye Dönüşmesi",
        "content": "Doku onarım mekanizmaları deride bir kesiyi kapatıp hayat kurtarırken; iç organlarda kronik bir hasara yanıt olarak devreye girdiğinde ölümcül bir yıkıma yol açar:\n\n- **Fibrozis vs Skar:**\n  - Skar genellikle lokalize bir hasar sonrası oluşan sınırlı bağ dokusu yamasıdır.\n  - **Fibrozis ise parankimal organlarda (karaciğer, akciğer, böbrek, kalp) kronik ve kontrolsüz kollajen birikimiyle organın mimarisini ve fonksiyonunu yok eden sistemik bir patolojidir**.\n- **Ortak İmmünolojik Yolak:**\n  - Kronik enflamasyon -> M2 makrofajlar ve lenfositler -> Sürekli ve aşırı **TGF-β** salınımı -> Yerleşik mezenkimal hücrelerin (stellat hücreler, perisitler) miyofibroblasta dönüşmesi -> Masif Tip I ve Tip III kollajen depolanması.\n- **Sonuç:** Yumuşak, süngerimsi ve işlevsel parankim dokuları taş gibi sert, büzüşmüş ve kanlanamayan fibröz organlara döner.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Fizyolojik Deri Skarı vs Ölümcül Parankimal Organ Fibrozisi",
                "Deri Skarı (Sınırlı ve Faydalı)",
                "Kesiyi kapatır, anatomik bütünlüğü ve gerilme direncini sağlar; hayatı tehdit etmez.",
                "Organ Fibrozisi (Siroz / Pulmoner Fibrozis)",
                "Karaciğer veya akciğer parankimini sert kollajenle boğarak son dönem organ yetmezliğine ve ölüme yol açar."
            ),
            make_cloze(
                "Parankimal organlarda kronik hasara yanıt olarak aşırı ve kontrolsüz kollajen birikmesi tablosuna fibrozis denir.",
                "fibrozis",
                "İç organlardaki patolojik bağ dokusu birikimi terimi"
            )
        ]
    })

    # Slide 92
    slides.append({
        "id": "k1-15-s92",
        "title": "Karaciğer Sirozu: Stellat Hücreler ve Disse Aralığı Fibrozisi",
        "content": "Parankimal organ fibrozisinin dünyadaki en sık ve en ölümcül örneği karaciğer sirozudur (Sınav Spotu):\n\n- **Kilit Hücresel Aktör: Hepatik Stellat Hücreler (İto Hücreleri):**\n  - Normal karaciğerde Disse aralığında sessizce otururlar ve vücudun **A vitamini deposu** olarak görev yaparlar.\n- **Fibrojenik Dönüşüm:**\n  - Kronik Hepatit B, C virüsleri veya kronik alkol hasarında; Kupffer hücrelerinden ve hepatositlerden yoğun **TGF-β** ve **PDGF** salınır.\n  - Stellat hücreler A vitamini damlacıklarını kaybeder ve yüksek oranda **alfa-düz kas aktini (α-SMA)** eksprese eden proliferatif **miyofibroblastlara** dönüşürler.\n- **Disse Aralığının Tıkanması (Sinüzoid Kapillerizasyonu):**\n  - Miyofibroblastlar Disse aralığına yoğun Tip I ve Tip III kollajen yığar.\n  - Sinüzoidlerin endotelindeki doğal pencereler (fenestralar) kapanır; kan ile hepatosit arasındaki madde alışverişi felç olur.\n- **Sonuç: Rejenerasyon Nodülleri ve Portal Hipertansiyon:** Karaciğer nodüler sert bir kitleye döner, portal ven basıncı fırlar ve özofagus varis kanamaları başlar.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Karaciğer Sirozunun Hücresel Fibrogenez Zinciri",
                [
                    "1. Kronik Parankim Hasarı: Alkol veya virüs hepatosit ölümünü ve nekrozu tetikler.",
                    "2. Kupffer Sitokin Fırtınası: Makrofajlar yoğun TGF-beta ve PDGF salgılar.",
                    "3. Stellat Hücre Aktivasyonu: İto hücreleri A vitaminini kaybedip miyofibroblasta döner.",
                    "4. Disse Aralığı Kollajenizasyonu: Tip I kollajen sinüzoid pencerelerini kapatır (kapillerizasyon).",
                    "5. Siroz ve Portal Hipertansiyon: Fibröz septalarla çevrili rejenerasyon nodülleri oluşur."
                ]
            ),
            make_quiz(
                "Karaciğer sirozunda kronik hepatit veya alkol hasarına bağlı olarak A vitamini depolayan durağan halden kollajen üreten aktif miyofibroblasta dönüşen kilit hücre tipi hangisidir?",
                [
                    {"key": "A", "text": "Hepatik Stellat Hücre (İto Hücresi)", "isCorrect": True, "explanation": "Doğru cevap A'dır: Karaciğer fibrogenezinin ana hücresi Disse aralığında yer alan ve miyofibroblasta dönüşen hepatik stellat (İto) hücreleridir."},
                    {"key": "B", "text": "Kupffer hücresi", "isCorrect": False, "explanation": "Kupffer hücreleri makrofajdır; sitokin salgılar ancak asıl kollajeni stellat hücreler üretir."},
                    {"key": "C", "text": "Safra kanalı kolanjiyositi", "isCorrect": False, "explanation": "Kolanjiyosit safra epiteli hücresidir."},
                    {"key": "D", "text": "Eritrosit", "isCorrect": False, "explanation": "Kırmızı kan hücresidir."}
                ]
            )
        ]
    })

    # Slide 93
    slides.append({
        "id": "k1-15-s93",
        "title": "İdiyopatik Pulmoner Fibrozis (IPF) ve 'Bal Peteği' Akciğer",
        "content": "Akciğer parankiminde ilerleyici, ölümcül ve geri dönüşsüz bağ dokusu birikimi tablosudur:\n\n- **Etiyopatogenez (Sınav Spotu):**\n  - Genetik yatkınlığı olan bireylerde tekrarlayan mikroskobik alveolar epitel hasarları (sigara, reflü, toz maruziyeti).\n  - Tip I pnömositler ölür; Tip II pnömositler hasarı onarmaya çalışırken kontrolsüz **TGF-β** ve **FGF** salgılar.\n  - İnterstisyumdaki fibroblastlar aşırı prolifere olarak **'Fibroblastik Odaklar' (Fibroblastic Foci)** oluşturur.\n- **Kollajen Fırtınası ve Matriks Yıkımı:**\n  - Alveol duvarları kalın Tip I kollajenle dolar; gaz difüzyon mesafesi 10 katına çıkar.\n- **Morfoloji: 'Bal Peteği Akciğer' (Honeycomb Lung):**\n  - Alveoler mimari tamamen çöker; akciğer genişlemiş kistik boşluklar ve aralarındaki kalın fibröz bantlardan oluşan bir bal peteğine döner.\n- **Klinik Tablo:** İlerleyici efor dispnesi, kuru öksürük ve hipoksemi; ortalama yaşam süresi akciğer nakli yapılmazsa 3-5 yıldır.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Normal İnce Alveol Duvarı vs Fibröz Bal Peteği Akciğer",
                "Normal Akciğer (Kusursuz Gaz Değişimi)",
                "Tek katlı yassı Tip I pnömositler ve incecik kılcallar; gaz alışverişi milisaniyeler sürer.",
                "Bal Peteği Akciğer (İdiyopatik Pulmoner Fibrozis)",
                "Alveoller kollajenle tıkanmış, kistik delikler açılmış ve gaz difüzyonu tamamen durmuştur."
            ),
            make_cloze(
                "İdiyopatik pulmoner fibrozisin ileri evresinde akciğer mimarisinin kistik boşluklar ve kalın fibröz bantlara dönmesine bal peteği akciğer denir.",
                "peteği",
                "Kistik son dönem akciğer morfolojisinin benzetme adı"
            )
        ]
    })

    # Slide 94
    slides.append({
        "id": "k1-15-s94",
        "title": "Böbrek ve Kalpte Fibrozis: Glomerüloskleroz ve Post-MI Skar",
        "content": "Fibrozis vücudun hangi organında gelişirse gelişsin daima 'işlevsel parankimin ölümü ve yerine sert bağ dokusunun çökmesi' kuralını takip eder:\n\n- **Böbrekte Fibrozis (Son Dönem Böbrek Yetmezliği):**\n  - Diyabetik nefropati veya kronik glomerülonefritte glomerüllerde ve tübülointerstisyel alanda aşırı kollajen depolanır.\n  - Glomerüller süzme yeteneğini kaybederek asellüler pembe yumaklara döner (**Glomerüloskleroz**).\n  - Tübüller atrofiye uğrar; son dönem böbrek küçülmüş, yüzeyi pürtüklü sert bir taş haline gelir.\n- **Kalpte Post-Enfarktüs Skarı (Miyokardiyal Fibrozis):**\n  - Koroner tıkanıklığıyla ölen kardiyak miyositler rejenere olamaz.\n  - Makrofaj temizliğini takiben granülasyon dokusu gelişir ve 6-8 haftada yerini **yoğun beyaz kollajenöz skar plaklarına** bırakır.\n  - Bu skar alanı kasılamaz; ventrikül genişler (remodeling) ve kalp yetmezliği gelişir.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Organ", "Kronik Tetikleyici", "Fibrojenik Hücre", "Nihai Patolojik Tablo"],
                [
                    ["Karaciğer", "Alkol, Hepatit B/C", "Hepatik Stellat Hücre (İto)", "Siroz ve Portal Hipertansiyon"],
                    ["Akciğer", "Sigara, İdiopatik", "İnterstisyel Fibroblast", "Bal Peteği Akciğer (IPF)"],
                    ["Böbrek", "Diyabet, Hipertansiyon", "Mezanjiyal ve İnterstisyel hücre", "Glomerüloskleroz ve Üremi"],
                    ["Kalp", "Koroner Tıkanıklığı / MI", "Kardiyak Fibroblast", "Miyokard Skarı ve Kalp Yetmezliği"]
                ]
            ),
            make_recall(
                "Kronik böbrek yetmezliğinde glomerüllerin ve tübüllerin yerini yoğun bağ dokusunun alması sürecine ne ad verilir?",
                "Glomerüloskleroz ve interstisyel fibrozistir (nefroskleroz)."
            )
        ]
    })

    # Slide 95
    slides.append({
        "id": "k1-15-s95",
        "title": "Ders Notu Eki: Transplantasyon İmmünolojisi ve Rejeksiyon Tipleri",
        "content": "Doku onarımı ve organ nakillerinin kesiştiği noktada, allogreftlerin reddedilme süreçleri yer alır (Ders Notu Özel Eki):\n\n- **1. Hiperakut Rejeksiyon (Dakikalar - Saatler İçinde):**\n  - **Mekanizma:** Alıcıda önceden var olan donör antijenlerine karşı antikorlar (Anti-HLA veya ABO antikorları).\n  - **Patoloji:** Damar endoteline bağlanan antikorlar komplemanı aktive eder; yaygın trombotik tıkanma, fibrinoid nekroz ve greftin dakikalar içinde morarıp ölmesi.\n- **2. Akut Rejeksiyon (Günler - Haftalar - Aylar İçinde):**\n  - **Akut Sellüler Rejeksiyon:** Alıcının CD8+ sitotoksik T lenfositleri donör parankimini ve endotelini doğrudan öldürür (endotelit ve interstisyel lenfosit infiltrasyonu).\n  - **Akut Humoral (Antikor Aracılı) Rejeksiyon:** Donöre karşı gelişen yeni antikorlar peritübüler kapillerlerde **C4d kompleman birikimine** yol açar.\n- **3. Kronik Rejeksiyon (Aylar - Yıllar İçinde):**\n  - T hücreleri ve sitokinlerin uyardığı intimal düz kas proliferasyonu sonucu damarlar daralır (**hızlanmış damar sklerozu / graft vaskülopatisi**) ve parankim iskemiyle atrofiye uğrayıp yaygın **fibrozis** ile kaybedilir.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Rejeksiyon Türü", "Zaman Çizelgesi", "Temel İmmün Mekanizma", "Histopatolojik Karakter"],
                [
                    ["Hiperakut", "Dakikalar / Saatler", "Önceden var olan antikorlar + Kompleman", "Damar trombozu ve fibrinoid nekroz"],
                    ["Akut Sellüler", "Günler / Haftalar", "Alıcı CD8+ T lenfositleri", "İnterstisyel lenfosit infiltrasyonu ve tübülit"],
                    ["Akut Humoral", "Günler / Haftalar", "Donöre özgü yeni antikorlar", "Peritübüler kapillerlerde C4d depolanması"],
                    ["Kronik", "Aylar / Yıllar", "Kronik sitokin uyarımı ve vaskülopati", "İntimal fibrozis, lümen darlığı ve organ sklerozu"]
                ]
            ),
            make_quiz(
                "Böbrek nakli yapılan bir hastada operasyondan aylar sonra yavaş yavaş gelişen, damar intima tabakasında düz kas proliferasyonu ve yaygın parankim fibrozisi ile giden rejeksiyon tipi hangisidir?",
                [
                    {"key": "A", "text": "Hiperakut rejeksiyon", "isCorrect": False, "explanation": "Hiperakut dakikalar içinde trombozla seyreder."},
                    {"key": "B", "text": "Kronik rejeksiyon (Graft vaskülopatisi ve fibrozis)", "isCorrect": True, "explanation": "Doğru cevap B'dir: Kronik rejeksiyon aylar-yıllar içinde damar intiması kalınlaşması (skleroz) ve parankimin yaygın fibrozisi ile seyreder."},
                    {"key": "C", "text": "Akut sellüler rejeksiyon", "isCorrect": False, "explanation": "Akut sellülerde CD8+ lenfositler tübülleri infiltre eder."},
                    {"key": "D", "text": "Fizyolojik rejenerasyon", "isCorrect": False, "explanation": "Rejeksiyon patolojik bir doku reddidir."}
                ]
            )
        ]
    })

    # Slide 96
    slides.append({
        "id": "k1-15-s96",
        "title": "Graft-Versus-Host Hastalığı (GVHD): Donörün Alıcıyı Kemirmesi",
        "content": "Kemik iliği (hematopoetik kök hücre) nakillerinde organ reddinin tam tersi bir felaket yaşanır:\n\n- **GVHD Tanımı (Sınav Spotu):** Nakledilen donör kemik iliğindeki yetkin immün hücrelerin (T lenfositlerinin), immünitesi baskılanmış alıcının dokularını 'yabancı' tanıyarak saldırması durumudur.\n- **Şartları (Billingham Kriterleri):**\n  1. Greft immünolojik olarak yetkin T hücreleri içermelidir.\n  2. Alıcı dokuları donörden farklı antijenler (HLA uyuşmazlığı) taşımalıdır.\n  3. Alıcı immünsüprese olmalı ve grefti reddedememelidir.\n- **Hedef Organlar (Üçlü Klasik Hedef):**\n  - **Deri:** Yaygın makülopapüler döküntüler, soyulma (büllöz nekroz / toksik epidermal nekroliz benzeri).\n  - **Gastrointestinal Sistem:** Şiddetli sulu-kanlı diyare, kramplar, mukoza dökülmesi.\n  - **Karaciğer:** Safra kanalları nekrozu, sarılık ve kolestaz.\n- **Kronik GVHD:** Sklerodermaya benzer yaygın cilt sertleşmesi ve otoimmün benzeri fibrozisle seyreder.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Organ Rejeksiyonu vs Graft-Versus-Host Hastalığı (GVHD)",
                "Organ Rejeksiyonu (Alıcı -> Donöre)",
                "Alıcının bağışıklık sistemi nakledilen böbrek veya karaciğeri yabancı görüp reddeder.",
                "GVHD (Donör -> Alıcıya)",
                "Nakledilen kemik iliğindeki yabancı donör T hücreleri alıcının tüm vücuduna (deri, bağırsak, karaciğer) saldırır."
            ),
            make_cloze(
                "Kemik iliği nakli sonrasında donör T lenfositlerinin alıcının deri, karaciğer ve bağırsaklarına saldırması tablosuna Graft-Versus-Host Hastalığı denir.",
                "Host",
                "GVHD kısaltmasındaki alıcı konak kelimesi"
            )
        ]
    })

    # Slide 97
    slides.append({
        "id": "k1-15-s97",
        "title": "Anti-Fibrotik Tedaviler: Modern Tıbbın Yeni Ufku",
        "content": "Geçmişte fibrozis 'geri dönüşümsüz bir son durak' olarak kabul edilirdi; ancak modern moleküler patoloji fibrozisi durduracak ve geriletecek ilaçlar geliştirmiştir:\n\n- **1. TGF-β Hedefli Tedaviler:**\n  - TGF-β antikorları veya reseptör kinaz inhibitörleri; fibrozis sinyalini kaynağında kesmeyi hedefler.\n- **2. Pirfenidon (Pulmoner Fibrozis İlacı):**\n  - TGF-β üretimini ve fibroblast proliferasyonunu baskılar; akciğer fibrozisinin ilerlemesini yavaşlatır.\n- **3. Nintedanib (Çoklu Tirozin Kinaz İnhibitörü):**\n  - PDGF, FGF ve VEGF reseptörlerini aynı anda bloke eder; fibroblast aktivasyonunu ve anjiyogenezi durdurur.\n- **4. Sirozun Geri Dönüşebilirliği:**\n  - Hepatit C hastalarında yeni direkt etkili antivirallerle (DAA) virüs tamamen temizlendiğinde; karaciğerdeki MMP/TIMP dengesi MMP lehine döner ve erken evre fibröz septalar yıllar içinde eriyerek karaciğer rejenere olabilir!",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Anti-Fibrotik Strateji", "Örnek İlaç", "Hedeflenen Moleküler Yolak", "Klinik Endikasyon"],
                [
                    ["Tirozin Kinaz Blokajı", "Nintedanib", "PDGFR, FGFR, VEGFR reseptörleri", "İdiyopatik Pulmoner Fibrozis"],
                    ["Sitokin Sentez İnhibisyonu", "Pirfenidon", "TGF-beta ve kollajen transkripsiyonu", "Pulmoner Fibrozis"],
                    ["Etiyolojik Eradikasyon", "DAA Antiviralleri", "HCV klirensi ile fibrozisin gerilemesi", "Karaciğer Sirozu"]
                ]
            ),
            make_recall(
                "Modern tıpta karaciğer sirozunun erken evrelerinde etken (örneğin Hepatit C) tamamen yok edildiğinde fibrozisin gerileyebilmesinin hücresel mekanizması nedir?",
                "TGF-beta uyarısı kesildiği için stellat hücrelerin inaktif hale geçmesi, TIMP düzeyinin düşmesi ve MMP enzimlerinin birikmiş kollajen septalarını yavaş yavaş sindirmesidir."
            )
        ]
    })

    # Slide 98
    slides.append({
        "id": "k1-15-s98",
        "title": "Tıp Hekiminin Yara Bakımı ve Doku Onarımındaki 5 Altın Kuralı",
        "content": "Geleceğin klinisyenleri olarak yara yönetimi hekimlik sanatının en somut vitrinidir:\n\n- **1. Asepsi ve Debridman:** Enfeksiyon ve nekrotik doku varken hiçbir yara iyileşemez; önce temizle, sonra kapat.\n- **2. Gerilimsiz Kapatma (No Tension):** Yaranın kenarlarını aşırı gererek dikmeyin; gerilim kan akımını bozar, iskemi yapar ve dehisense yol açar.\n- **3. Dokuya Nazik Davranma (Halsted İlkeleri):** Dokuyu ezmeyin, yakmayın, gereksiz koterize etmeyin; her ölü hücre granülasyon yükünü artırır.\n- **4. Beslenme ve Altta Yatan Hastalığı Yönetme:** Kan şekerini regüle edin, hastaya protein, C vitamini ve çinko desteği sağlayın.\n- **5. Aşırı Skara Karşı Uyanık Olma:** Genetik yatkınlığı olan hastalarda keloid ve kontraktür riskini baştan öngörün ve gereksiz cerrahi travmalardan kaçının.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Kaba ve Bilinçsiz Cerrahi Müdahale vs Halsted İlkelerine Uygun Nazik Cerrahi",
                "Kaba Cerrahi (Ezilmiş Doku)",
                "Aşırı koter nekrozu, gergin dikişler; yara dehisensi, apse veya devasa kaba skar ile sonlanır.",
                "Halsted İlkeleri (Nazik Yaklaşım)",
                "Mükemmel hemostaz, gerilimsiz sütür, doku saygısı; estetik, güçlü ve sorunsuz primer iyileşme sağlar."
            ),
            make_cloze(
                "Cerrahi doku onarımında gerilimsiz sütür, mükemmel hemostaz ve dokuya nazik yaklaşımı tanımlayan klasik cerrahi kurallara Halsted ilkeleri denir.",
                "Halsted",
                "Modern nazik cerrahinin kurucusunun adı"
            )
        ]
    })

    # Slide 99
    slides.append({
        "id": "k1-15-s99",
        "title": "Bütüncül Klinik Patoloji Simülasyonu: Ağır Travma Sonrası Onarım Yönetimi",
        "content": "Trafik kazası geçiren 30 yaşındaki bir hastada karaciğer laserasyonu, açık uyluk yaralanması ve üçüncü derece derin yanıklar bulunuyor:\n\n- **Karaciğer Hasarı:** Karaciğerin sol lobu cerrahi olarak çıkarılıyor. Stabil doku kuralları gereği, sağlam sağ lobdaki hepatositler Kupffer hücrelerinin TNF/IL-6 (priming) ve HGF (proliferasyon) uyarısıyla 3 haftada kütlesini tamamlıyor; rejenerasyon gerçekleşiyor.\n- **Açık Uyluk Yarası:** Doku kaybı çok geniş olduğu için sekonder iyileşmeye bırakılıyor; yara tabanından fışkıran pembe granülasyon dokusu (anjiyogenez ve fibroblastlar) ve miyofibroblast kontraksiyonuyla 6 haftada kapanıyor.\n- **Derin Yanık Alanı:** Boyundaki yanık skarı iyileşirken miyofibroblastlar aşırı kasılarak çeneyi göğse bağlayan patolojik bir **kontraktür** oluşturuyor; plastik cerrahi Z-plasti ile bu kontraktürü gevşetiyor.\n- **Sonuç:** Organizmanın tüm onarım mekanizmaları tek bir vakada eşzamanlı olarak hayat kurtarır ve yönetilir.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_branching(
                "Klinik Karar: Polistravmalı Hastada Çoklu Onarım Stratejisi",
                "Hastanın uyluğundaki açık, kirli, toprak bulaşmış 15 cm'lik yarayı acilde hemen ipek dikişlerle sıkıca kapatmak isteyen asistan hekime karşı uzman hekimin tavrı ne olmalıdır?",
                [
                    {
                        "text": "'Haklısın, yara ne kadar çabuk dikilirse o kadar hızlı rejenere olur.'",
                        "outcome": "Ölümcül hata: Toprak ve anaerop bakteriler içeride kilitlenir; hasta 48 saat içinde klostridyal gazlı kangren ve sepsisle kaybedilir.",
                        "isCorrect": False
                    },
                    {
                        "text": "'Kesinlikle primer kapatılamaz! Yara derhal ameliyathanede bol SF ile yıkanmalı, tüm nekrotik dokular debride edilmeli; enfeksiyon kontrolü için açık bırakılarak sekonder veya tersiyer iyileşmeye hazırlanmalıdır.'",
                        "outcome": "Kusursuz travma cerrahisi kararı: Enfeksiyon ve kangren önlenir, güvenli onarım sağlanır.",
                        "isCorrect": True
                    },
                    {
                        "text": "'Yaraya hiç dokunmayıp sadece merhem sürelim.'",
                        "outcome": "Ağır tıbbi kusur.",
                        "isCorrect": False
                    }
                ]
            ),
            make_quiz(
                "Bu travma simülasyonunda boyundaki derin yanık skarının hastanın baş hareketlerini kilitleyecek şekilde aşırı büzüşmesine yol açan hücre ve patolojik antite hangisidir?",
                [
                    {"key": "A", "text": "Miyofibroblastlar ve kontraktür", "isCorrect": True, "explanation": "Doğru cevap A'dır: Yanık skarlarında miyofibroblastların aşırı kasılmasıyla eklem hareketlerini kısıtlayan patolojik büzülmelere kontraktür denir."},
                    {"key": "B", "text": "Hepatositler ve siroz", "isCorrect": False, "explanation": "Hepatositler boyunda bulunmaz."},
                    {"key": "C", "text": "Plazma hücreleri ve multipl miyelom", "isCorrect": False, "explanation": "Hematolojik malignitedir."},
                    {"key": "D", "text": "Endotel hücreleri ve hemanjiyom", "isCorrect": False, "explanation": "Benign vasküler tümördür."}
                ]
            )
        ]
    })

    # Slide 100 - CHECKPOINT 10 / BÜTÜNCÜL ÖZET
    slides.append({
        "id": "k1-15-s100",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 10] Doku Onarımı ve Yara İyileşmesi Bütüncül Özeti",
        "content": "Bu son checkpointte Ders 15'in tüm patolojik, hücresel ve moleküler mekanizmalarını tek bir vizyonda birleştiriyoruz:\n\n- **1. Onarım Yolları:** Rejenerasyon (orijinal hücre çoğalması, ECM sağlam olmalı) vs Skarla Onarım (kollajen bağ dokusu yaması).\n- **2. Doku Sınıflaması:** Labil (GIS epiteli, kemik iliği, deri), Stabil / G0 (Karaciğer hepatositleri, böbrek tübülleri), Kalıcı (Kalp kası, nöronlar).\n- **3. Karaciğer Rejenerasyonu:** Priming (Kupffer -> TNF/IL-6), Proliferasyon (HGF / c-Met), Terminasyon (TGF-β), Oval kök hücreler.\n- **4. Skarla Onarımın 4 Evresi:** Hemostaz -> Enflamasyon (Nötrofil ilk 24h, Makrofaj 48-72h) -> Proliferasyon (Granülasyon) -> Remodeling.\n- **5. M1 vs M2 Makrofaj:** M1 yıkıcı/savaşçı; M2 (IL-4/IL-13) TGF-β ve VEGF salan yapıcı/onarıcı orkestra şefi.\n- **6. Granülasyon Dokusu:** Yeni kapillerler (anjiyogenez) + Fibroblastlar + Gevşek ödemli ECM. (Granülomatöz iltihap ile asla karıştırılamaz!).\n- **7. Anjiyogenez:** Tip hücresi (VEGF göçü), Stalk hücresi (Notch/Dll4 denetimi), Ang-1/Tie-2 ve PDGF (perisit stabilizasyonu).\n- **8. Kollajen ve TGF-beta:** Erken Tip III -> Geç Tip I dönüşümü. C vitamini (hidroksilasyon), Bakır (lizil oksidaz çapraz bağ). TGF-β: En güçlü fibrogenik faktör (kollajen artar, MMP düşer, TIMP artar).\n- **9. İyileşme Tipleri:** Primer (temiz dikişli, az skar), Sekonder (açık yara, belirgin miyofibroblast kontraksiyonu %70-80, kaba skar), Tersiyer (gecikmiş sütür).\n- **10. Anormal İyileşme:** Dehisens (açılma), Hipertrofik skar (sınırda kalır, geriler), Keloid (sınırları aşar, Tip I kollajen, gerilemez, nüks eder), Kontraktür (yanık büzüşmesi), Parankimal Organ Fibrozisi (Siroz, İto hücreleri; IPF).",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Ders Bölümü", "Anahtar Molekül / Hücre", "Temel Biyolojik / Patolojik Rol"],
                [
                    ["Doku Kapasitesi", "Labil / Stabil / Kalıcı", "Rejenerasyon şansını belirleyen hücre döngüsü durumu"],
                    ["Karaciğer Büyümesi", "HGF (c-Met) ve TGF-beta", "Kompansatuvar hiperplazinin gaz ve fren pedalları"],
                    ["Orkestra Şefi", "M2 Makrofaj (IL-4 / IL-13)", "Enflamasyonu söndürüp büyüme faktörleriyle onarımı başlatma"],
                    ["Anjiyogenez", "VEGF-A, Notch/Dll4, Ang-1", "Yeni kapiller tomurcuklanması ve perisit stabilizasyonu"],
                    ["Fibrogenez", "TGF-beta ve Tip I Kollajen", "En güçlü fibrogenik sitokin; skar ve organ fibrozisi yapımı"],
                    ["Yara Gücü", "MMP / TIMP, Lizil Oksidaz", "1. haftada %10; 3. ayda maksimum %70-80 plato sınırı"],
                    ["Aşırı Skar", "Keloid vs Hipertrofik Skar", "Yara sınırını aşma, gerilememe ve genetik yatkınlık farkı"]
                ]
            ),
            make_chain(
                "Doku Onarımının 5 Büyük Biyolojik İlkesi",
                [
                    "1. Hücre ve ECM Dengesi: Rejenerasyon ancak hücre çoğalabilir ve ECM çatısı sağlamsa gerçekleşir.",
                    "2. Makrofaj Liderliği: Nötrofil temizliğinden sonra M2 makrofajlar büyüme faktörlerini salar.",
                    "3. Granülasyon Köprüsü: VEGF ile yeni damarlar ve PDGF ile fibroblastlar doku boşluğunu doldurur.",
                    "4. Kollajen Olgunlaşması: C vitamini ve bakır desteğiyle Tip III kollajen sağlam Tip I'e döner.",
                    "5. Remodeling Sınırı: MMP ve TIMP dengesiyle skar olgunlaşır; yara gücü maksimum %70-80'e ulaşır."
                ]
            )
        ]
    })

    return slides
