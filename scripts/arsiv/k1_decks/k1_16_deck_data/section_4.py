# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_4_slides():
    slides = []

    # Slide 31
    slides.append({
        "id": "k1-16-s31",
        "title": "Ödemin Beş Temel Mekanizması: Patolojik Sınıflandırma",
        "content": "İnterstisyel doku aralığında aşırı sıvı birikimi (ödem), Starling dengesini ve lenfatik klirensi bozan beş temel patofizyolojik süreçten kaynaklanır (Sınav Spotu):\n\n- **1. Artmış Kapiller Hidrostatik Basınç:** Venöz dönüşün bozulması veya arteriyoler genişleme sonucu sıvının damar dışına itilmesi.\n- **2. Azalmış Plazma Onkotik Basıncı (Hipoproteinemi):** Albümin kaybı veya sentez azlığı nedeniyle sıvının damar içinde tutulamaması.\n- **3. Lenfatik Obstrüksiyon (Lenfödem):** İnterstisyel sıvıyı drene eden lenf yollarının mekanik veya neoplastik tıkanması.\n- **4. Sodyum ve Su Retansiyonu:** Böbreklerden tuz ve su atılamaması sonucu intravasküler hacmin aşırı genişlemesi.\n- **5. Artmış Vasküler Permeabilite (Enflamatuvar Ödem):** Akut veya kronik yangıda endotel hücre aralıklarının açılması (eksuda oluşumu).",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Ödem Mekanizması", "Temel Patofizyolojik Değişim", "Karakteristik Klinik Örnek"],
                [
                    ["Artmış Hidrostatik Basınç", "Venöz göllenme, geri tepen kapiller basınç", "Konjestif kalp yetmezliği, derin ven trombozu"],
                    ["Azalmış Onkotik Basınç", "Hipoalbüminemi (<2.5 g/dL)", "Nefrotik sendrom, karaciğer sirozu, kwashiorkor"],
                    ["Lenfatik Tıkanma", "Doku sıvısı klirensinin durması", "Meme cerrahisi sonrası lenfödem, filaryazis"],
                    ["Sodyum ve Su Retansiyonu", "Aşırı intravasküler hacim yükü", "Akut glomerülonefrit, böbrek yetmezliği"],
                    ["Artmış Geçirgenlik", "Endotel hasarı ve mediyatör etkisi", "Akut enflamasyon, yanık, anjiyoödem"]
                ]
            ),
            make_quiz(
                "Aşağıdakilerden hangisi ödem oluşumuna yol açan 5 temel fizyopatolojik mekanizmadan biri değildir?",
                [
                    {"key": "A", "text": "Plazma kolloid ozmotik basıncının aşırı yükselmesi", "isCorrect": True, "explanation": "Doğru cevap A'dır: Plazma onkotik basıncının artması sıvıyı damar içine çeker, ödemi azaltır. Ödem onkotik basıncın 'azalması' ile oluşur."},
                    {"key": "B", "text": "Kapiller hidrostatik basıncın venöz stazla artması", "isCorrect": False, "explanation": "Bu temel ödem mekanizmalarından biridir."},
                    {"key": "C", "text": "Lenf kanallarının tümör veya cerrahiyle tıkanması", "isCorrect": False, "explanation": "Lenfatik drenaj bozulması ödem yapar."},
                    {"key": "D", "text": "Böbreklerden sodyum ve suyun tutulması (retansiyon)", "isCorrect": False, "explanation": "Hacim yükü ödemi kolaylaştırır."}
                ]
            )
        ]
    })

    # Slide 32
    slides.append({
        "id": "k1-16-s32",
        "title": "Artmış Hidrostatik Basıncın Etiyolojisi ve Mekanizmaları",
        "content": "Kapiller hidrostatik basınç artışı, sıvı çıkışını en güçlü tetikleyen faktördür:\n\n- **1. Bozulmuş Venöz Dönüş (En Sık Neden):**\n  - Kanın venöz yataktan kalbe geri akışı engellendiğinde, geriye doğru venüller ve kapillerlerde hidrostatik basınç hızla yükselir.\n  - Sistemik Nedenler: Konjestif kalp yetmezliği, konstriktif perikardit, yaygın assit varlığı.\n  - Lokalize Nedenler: Derin ven trombozu, venöz kompresyon (tümör basısı, gebelik rahminin basısı), uzun süre ayakta hareketsiz kalma (yerçekimi etkisi).\n- **2. Arteriyoler Genişleme (Artmış Giriş Akımı):**\n  - Aşırı sıcak ortam maruziyeti veya nörohümoral vasküler tonus bozukluğunda arterioller aşırı gevşer; kapiller yatağa giren kan debisi ve basıncı artarak filtrasyonu hızlandırır.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Sistemik Venöz Basınç Artışı vs Lokalize Venöz Basınç Artışı",
                "Sistemik Venöz Basınç Artışı",
                "Kalp yetmezliğine bağlıdır; bilateral bacak ödemi, karaciğer büyümesi ve boyun ven dolgunluğu eşlik eder.",
                "Lokalize Venöz Basınç Artışı",
                "Tek bir vende tromboz veya basıya bağlıdır; yalnızca etkilenen ekstremitede asimetrik ödem oluşur."
            ),
            make_cloze(
                "Venöz geri dönüşün bozulması sonucu kapiller içi itici kuvvet olan hidrostatik basınç artarak sıvıyı interstisyuma iter.",
                "hidrostatik basınç",
                "Damar lümenindeki itici fiziksel kan basıncı"
            )
        ]
    })

    # Slide 33
    slides.append({
        "id": "k1-16-s33",
        "title": "Bölgesel Venöz Obstrüksiyon: Derin Ven Trombozu (DVT) Kliniği",
        "content": "Lokalize hidrostatik basınç artışının en çarpıcı klinik örneği alt ekstremite derin ven trombozudur:\n\n- **Patofizyoloji:** İmmobilizasyon (uzun uçak yolculuğu, yatağa bağımlılık) veya hiperkoagülabilite zemininde popliteal veya femoral venlerde trombüs oluşur.\n- **Lokal Hidrostatik Patlama:** Tıkanan venin distalindeki kılcal damarlarda venöz dönüş durur; kapiller hidrostatik basınç venül ucunda bile arteriyol düzeyine yaklaşır.\n- **Klinik Tablo:**\n  - Etkilenen bacakta ani başlayan tek taraflı (asimetrik) ağrılı şişlik, gerginlik ve ciltte hafif morarma/kızarıklık gözlenir.\n  - Karşı bacak tamamen normaldir (sistemik kalp/böbrek hastalıklarının iki taraflı ödeminden bu asimetri ile ayırt edilir).\n- **Kritik Tehlike:** Trombüsten kopan parçanın vena kavayı geçerek pulmoner emboliye yol açması ölümcül risktir.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Derin Ven Trombozunda Ödem Gelişim Aşamaları",
                [
                    "1. Venöz Trombüs Oluşumu: İmmobilite zemininde derin bacak veni pıhtıyla tıkanır.",
                    "2. Geriye Doğru Basınç Birikimi: Venöz drenaj durur, venüler hidrostatik basınç fırlar.",
                    "3. Kapiller Kaçak: Starling dengesi çöker ve interstisyel dokuya masif transuda akar.",
                    "4. Tek Taraflı Ağrılı Şişlik: Bacakta asimetrik ödem, gerginlik ve yürüme güçlüğü oluşur."
                ]
            ),
            make_quiz(
                "Uzun süreli uçak yolculuğu sonrası sol bacağında aniden tek taraflı belirgin şişlik, sertlik ve ağrı gelişen hastada ödemin primer mekanizması hangisidir?",
                [
                    {"key": "A", "text": "Karaciğerde albümin sentezinin aniden durması", "isCorrect": False, "explanation": "Hipoalbüminemi iki taraflı simetrik ödem yapar."},
                    {"key": "B", "text": "Derin ven trombozuna bağlı lokalize kapiller hidrostatik basınç artışı", "isCorrect": True, "explanation": "Doğru cevap B'dir: Tek taraflı akut bacak ödeminde primer mekanizma derin ven trombozunun yarattığı lokal venöz hidrostatik artıştır."},
                    {"key": "C", "text": "Sol bacakta lenf nodlarının doğuştan yokluğu", "isCorrect": False, "explanation": "Akut erişkin başlangıcı konjenital agenezi ile açıklanamaz."},
                    {"key": "D", "text": "İki taraflı böbrek yetmezliği gelişmesi", "isCorrect": False, "explanation": "Böbrek yetmezliği simetrik genel ödem yapar."}
                ]
            )
        ]
    })

    # Slide 34
    slides.append({
        "id": "k1-16-s34",
        "title": "Kalp Yetmezliğinde Ödem: Azalmış Kardiyak Debi ve İleri Yetersizlik",
        "content": "Konjestif kalp yetmezliğinde ödem oluşumu tek bir mekanizmayla değil, hemodinamik ve nörohümoral bir zincirle gerçekleşir:\n\n- **1. İleri Yetersizlik (Forward Failure):**\n  - Sol veya sağ ventrikülün miyokardiyal kasılma gücü düştüğünde sistemik arteriyel sisteme pompalanan dakikalık kan debisi (kardiyak debi) azalır.\n  - Sonuç: Dokular ve özellikle böbrekler yeterince kanlanamaz (renal hipoperfüzyon).\n- **2. Geri Yetersizlik (Backward Failure):**\n  - Ventrikül gelen kanı boşaltamadığı için kan atriyumlarda ve büyük venöz gövdelerde göllenir.\n  - Vena kava ve santral venöz basınç yükselir; bu basınç tüm periferik kılcal damarlara yansıyarak kapiller hidrostatik basıncı artırır.\n- **Kombinasyon:** Kalp yetmezliği hem hidrostatik basıncı artırarak sıvıyı dışarı iter hem de böbrekleri uyararak vücutta tuz ve su tutulmasına yol açar.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "İleri Kalp Yetersizliği vs Geri Kalp Yetersizliği Etkisi",
                "İleri Yetersizlik (Forward Failure)",
                "Kardiyak debi düşer, böbrek perfüzyonu azalır; RAAS uyarılır ve sodyum-su tutulumu tetiklenir.",
                "Geri Yetersizlik (Backward Failure)",
                "Venöz sistemde kan birikir, sistemik hidrostatik basınç yükselir ve sıvı interstisyuma kaçar."
            ),
            make_cloze(
                "Kalp yetmezliğinde kalbin dokulara yeterli debi pompalayamaması sonucu böbrek perfüzyonunun azalmasına ileri yetersizlik denir.",
                "ileri yetersizlik",
                "Kardiyak debi düşüşüne bağlı perfüzyon azalması tablosu"
            )
        ]
    })

    # Slide 35
    slides.append({
        "id": "k1-16-s35",
        "title": "Renal Hipoperfüzyon ve RAAS Aktivasyonu",
        "content": "Kalp debisindeki düşüşü organizma 'kanama veya susuzluk' varmış gibi algılar:\n\n- **Jukstaglomerüler Yanıt:** Renal kan akımı ve glomerüler filtrasyon basıncı düşünce böbreğin jukstaglomerüler aparatındaki baroreseptörler uyarılır.\n- **Renin Salınımı:** Dolaşıma yüksek miktarda renin enzimi salgılanır.\n- **Anjiyotensin Kaskadı:**\n  - Renin, karaciğerden sentezlenen anjiyotensinojeni Anjiyotensin I'e çevirir.\n  - Akciğer endotelindeki ACE (Anjiyotensin Dönüştürücü Enzim) Anjiyotensin I'i güçlü bir vazokonstriktör olan **Anjiyotensin II**'ye dönüştürür.\n- **Etkiler:** Anjiyotensin II hem sistemik arteriolleri kasarak kan basıncını yükseltmeye çalışır hem de sürrenal korteksten **aldosteron** hormonunu salgılatır.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Renin-Anjiyotensin Kaskadının Aktivasyon Basamakları",
                [
                    "1. Kardiyak Debi Düşüşü: Böbrek glomerüllerine gelen perfüzyon basıncı kritik düzeye iner.",
                    "2. Renin Salınımı: Jukstaglomerüler hücreler kana yoğun renin enzimi verir.",
                    "3. Anjiyotensin II Üretimi: ACE enzimi Anjiyotensin I'i damar daraltıcı Anjiyotensin II'ye çevirir.",
                    "4. Aldosteron Salgılanması: Sürrenal korteks zona glomerulosadan aldosteron salınımı uyarılır."
                ]
            ),
            make_quiz(
                "Kalp yetmezliğinde böbrek hipoperfüzyonuna yanıt olarak jukstaglomerüler aparattan kana salgılanan primer enzim hangisidir?",
                [
                    {"key": "A", "text": "Pepsin", "isCorrect": False, "explanation": "Mide sindirim enzimidir."},
                    {"key": "B", "text": "Renin", "isCorrect": True, "explanation": "Doğru cevap B'dir: Düşük perfüzyon basıncı jukstaglomerüler hücrelerden renin salınımını tetikler."},
                    {"key": "C", "text": "Trombin", "isCorrect": False, "explanation": "Pıhtılaşma enzimidir."},
                    {"key": "D", "text": "Amilaz", "isCorrect": False, "explanation": "Pankreatik sindirim enzimidir."}
                ]
            )
        ]
    })

    # Slide 36
    slides.append({
        "id": "k1-16-s36",
        "title": "Sekonder Hiperaldosteronizm ve Sodyum/Su Retansiyonu",
        "content": "RAAS aktivasyonunun nihai sonucu böbrek tübüllerinde sodyum ve suyun tutulmasıdır:\n\n- **Sekonder Hiperaldosteronizm (Sınav Spotu):** Sürrenal bezin primer bir tümörü (Conn sendromu) olmadan, ekstra-adrenal bir uyaranla (burada kardiyak yetmezlik ve renin artışı) aldosteronun aşırı salgılanmasıdır.\n- **Tübüler Etki:** Aldosteron böbrek distal tübül ve toplayıcı kanallarındaki epitel hücrelerine etki eder; idrarla sodyum atılımını durdurarak lümenden kana **Na+ ve su geri emilimini** dramatik biçimde artırır; karşılığında K+ ve H+ atar.\n- **Plazma Hacim Genişlemesi:** Tutulan bu ek litrelerce sıvı intravasküler alana katılır.\n- **Fizyolojik Hedef vs Patolojik Gerçek:** Normalde bu mekanizma hipovolemik şokta hayat kurtarır; ancak kalbi zaten yetersiz çalışan hastada bu ek sıvı hacmi zayıf kalbi daha da ezer.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Primer Hiperaldosteronizm vs Sekonder Hiperaldosteronizm",
                "Primer Hiperaldosteronizm (Conn)",
                "Sürrenal korteks adenomu otonom aldosteron salgılar; renin düzeyi baskılanmıştır (düşüktür).",
                "Sekonder Hiperaldosteronizm",
                "Böbrek hipoperfüzyonuna yanıt olarak renin aşırı yüksektir; kalp yetmezliği ve sirozda tipiktir."
            ),
            make_cloze(
                "Kalp yetmezliğinde böbrek hipoperfüzyonunun uyardığı renin artışına bağlı aşırı aldosteron salınımına sekonder hiperaldosteronizm denir.",
                "sekonder hiperaldosteronizm",
                "Böbrek kökenli aşırı aldosteron uyarısı tablosu"
            )
        ]
    })

    # Slide 37
    slides.append({
        "id": "k1-16-s37",
        "title": "Kalp Yetmezliğindeki Kısır Döngü (Vicious Cycle)",
        "content": "Kalp yetmezliğinde ödem tablosunu derinleştiren ve kendi kendini besleyen patolojik döngü (kısır döngü) şöyle işler (Sınav Spotu):\n\n- **1. Kalp Debisi Düşer:** Hasta miyokard kanı pompalayamaz.\n- **2. RAAS Uyarılır:** Böbrek hipoperfüzyonu algılar, renin-aldosteron ile tuz ve suyu tutar.\n- **3. İntravasküler Hacim Artar:** Dolaşımdaki toplam sıvı miktarı artar.\n- **4. Venöz Basınç Tavan Yapar:** Kalbe dönen sıvı yükü (preload) aşırı artar; yetersiz kalp bu yükü boşaltamadığı için kapiller hidrostatik basınç daha da fırlar.\n- **5. Ödem Şiddetlenir:** Artan hidrostatik basınç sıvıyı interstisyuma iter; doku ödemi artar ancak damar içi efektif kan debisi yine yükselemez.\n- **Tedavi Mantığı:** Bu kısır döngüyü kırmak için hastalara idrar söktürücü (diüretikler: furosemid) ve RAAS blokerleri (ACE inhibitörleri) verilir.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Kalp Yetmezliğindeki Patolojik Kısır Döngü Basamakları",
                [
                    "1. Kardiyak Yetmezlik: Kalp kası kanı verimli pompalayamaz, debi düşer.",
                    "2. Böbrek Hipoperfüzyonu: Böbrekler kanlanamaz ve acil alarm verir.",
                    "3. RAAS ve Aldosteron: İdrarla atılacak sodyum ve su kana geri emilir.",
                    "4. Venöz Yüklenme ve Ödem: Aşırı sıvı venöz hidrostatik basıncı artırarak ödemi derinleştirir."
                ]
            ),
            make_quiz(
                "Konjestif kalp yetmezliğinde gelişen ödem tablosunda böbreklerin sodyum ve suyu tutarak kısır döngü yaratmasının nedeni hangisidir?",
                [
                    {"key": "A", "text": "Böbreklerin kalp kasını beslemek için aşırı protein üretmesi", "isCorrect": False, "explanation": "Böbrekler kalp için protein üretmez."},
                    {"key": "B", "text": "Kardiyak debi düşüşünü hipovolemi sanıp RAAS kaskadı ile tuz ve suyu geri emmesi", "isCorrect": True, "explanation": "Doğru cevap B'dir: Düşük debiyi kanama veya dehidratasyon sanan böbrek RAAS'ı çalıştırarak yetmezliği daha da kötüleştirir."},
                    {"key": "C", "text": "Hastanın aşırı miktarda kalsiyum kaybetmesi", "isCorrect": False, "explanation": "Kalsiyum kaybı bu döngünün sebebi değildir."},
                    {"key": "D", "text": "Akciğerlerin sodyumu doğrudan kana enjekte etmesi", "isCorrect": False, "explanation": "Akciğerler sodyum salgılamaz."}
                ]
            )
        ]
    })

    # Slide 38
    slides.append({
        "id": "k1-16-s38",
        "title": "Bağımlı (Dependent) Ödem ve Gode Bırakan (Pitting) Karakter",
        "content": "Kardiyak ve hidrostatik ödemin vücuttaki dağılımı yerçekimi kuvvetine doğrudan bağımlıdır:\n\n- **Bağımlı Ödem (Dependent Edema - Sınav Spotu):**\n  - Sıvı yerçekiminin etkisiyle vücudun anatomik olarak en altta kalan bölgelerine çöker.\n  - **Ayakta / Oturan Hastada:** Ödem öncelikle ayak bileklerinde, pretibial bölgede ve bacaklarda belirgindir.\n  - **Yatağa Bağımlı Hastada:** Sıvı yerçekimiyle arkaya kayar; **presakral bölge** ve uyluk arkasında toplanır.\n- **Gode Bırakan Ödem (Pitting Edema):**\n  - Başparmakla ödemli tibia kemiği üzerine 5-10 saniye bastırıldığında, interstisyel seröz sıvı çevre dokulara doğru kenara itilir.\n  - Parmak çekildiğinde geride belirgin bir **çukur (gode)** kalır ve çukurun yavaşça dolması saniyeler sürer.\n  - Lenfödem veya miksödemde ise dokuda protein ve glikozaminoglikan yoğun olduğundan çukur kalmaz (non-pitting).",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Ayakta Duran Hasta vs Yatağa Bağımlı Hasta Ödem Yerleşimi",
                "Ayakta Dolaşan Hasta",
                "Yerçekimi sıvıyı aşağı çeker; pretibial bölge ve ayak sırtında bilateral gode bırakan şişlik oluşur.",
                "Yatağa Bağımlı Hasta",
                "Yerçekimi sıvıyı arkaya çeker; bacaklar ince kalabilirken presakral alanda masif ödem birikir."
            ),
            make_cloze(
                "Kalp yetmezliğinde ödemli dokuya parmakla bastırıldığında sıvının kenara itilmesiyle oluşan geçici çukura gode bırakan ödem denir.",
                "gode bırakan",
                "Klinik muayenede parmak basısıyla çukurlaşan ödem karakteri"
            )
        ]
    })

    # Slide 39 - CHECKPOINT 4
    slides.append({
        "id": "k1-16-s39",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 4] Artmış Hidrostatik Basınç ve Kardiyak Ödem",
        "content": "Bu checkpointte hidrostatik basınç artışının nedenlerini ve kalp yetmezliğindeki nörohümoral yanıtı pekiştiriyoruz:\n\n- **Ödemin 5 Mekanizması:** Hidrostatik basınç ↑, Onkotik basınç ↓, Lenfatik obstrüksiyon, Sodyum/su retansiyonu, Artmış geçirgenlik.\n- **Bölgesel Hidrostatik Artış:** DVT gibi ven tıkanıklıklarında tek taraflı, asimetrik bacak ödemi gelişir.\n- **Sistemik Hidrostatik Artış:** Konjestif kalp yetmezliğinde venöz basınç genel olarak artar.\n- **Kardiyak Kısır Döngü:** Düşen debi $\\to$ Renal hipoperfüzyon $\\to$ RAAS uyarımı $\\to$ Sekonder hiperaldosteronizm $\\to$ Na+ ve su tutulumu $\\to$ Venöz yüklenme $\\to$ Şiddetlenen ödem.\n- **Bağımlı (Dependent) Ödem:** Ayakta pretibial, yatar pozisyonda presakral yerleşim; parmak basısıyla gode bırakır (pitting).",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Durum", "Ödem Dağılımı", "Mekanizma", "Gode Durumu"],
                [
                    ["Derin Ven Trombozu", "Tek taraflı alt ekstremite", "Lokal venöz tıkanıklık ve hidrostatik patlama", "Gode bırakır (pitting)"],
                    ["Konjestif Kalp Yetmezliği", "Bilateral simetrik, bağımlı (ayak/sakrum)", "Sistemik venöz staz ve sekonder hiperaldosteronizm", "Belirgin gode bırakır (pitting)"],
                    ["Lenfatik Tıkanma", "Genellikle tek kol veya bacak", "Lenf kanallarının mekanik tıkanması", "Erken dönemde gode bırakır, geç dönemde non-pitting"]
                ]
            ),
            make_chain(
                "Kardiyak Ödemin Fizyopatolojik Özeti",
                [
                    "1. Pompa Disfonksiyonu: Miyokard kanı ileri itemez.",
                    "2. İki Yönlü Hasar: Geriye venöz göllenme, ileriye böbrek iskemisi.",
                    "3. Sekonder Hiperaldosteronizm: Böbrek tuz ve suyu geri emerek venöz basıncı katlar.",
                    "4. Bağımlı Ödem: Yerçekimiyle bacaklarda veya presakral bölgede gode oluşur."
                ]
            )
        ]
    })

    # Slide 40
    slides.append({
        "id": "k1-16-s40",
        "title": "Bölüm Özeti: Hidrostatik Basınçtan Onkotik Basınca Geçiş",
        "content": "Bölüm 4'te kapiller hidrostatik basınç artışının hemodinamik temellerini ve kalp yetmezliğindeki RAAS kaskadını tamamladık:\n\n- **Önemli İlke:** Kalp yetmezliğinde sıvı birikimi sadece kalbin mekanik zayıflığıyla değil, böbreğin sodyum tutmasıyla devasa boyutlara ulaşır.\n- **Sonraki Bölüm:** Bir sonraki bölümde ödemin ikinci büyük mekanizması olan **azalmış plazma onkotik basıncını**, hipoalbüminemiyi, nefrotik sendromu ve karaciğer sirozunu inceleyeceğiz.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_recall(
                "Yatağa bağımlı kalp yetmezliği hastasında yerçekimi etkisiyle ödem sıvısının en çok biriktiği anatomik bölge neresidir?",
                "Presakral bölge (ve uyluk arkası)",
                "Kuyruk sokumu ve leğen kemiği arkasındaki bağımlı alan"
            ),
            make_quiz(
                "Kalp yetmezliği olan bir hastada gelişen sekonder hiperaldosteronizm tablosu idrar ve serum elektrolitlerinde ne tür bir değişime yol açar?",
                [
                    {"key": "A", "text": "İdrarla aşırı sodyum atılması ve plazma potasyumunun tehlikeli yükselmesi", "isCorrect": False, "explanation": "Aldosteron sodyumu tutar, potasyumu atar."},
                    {"key": "B", "text": "Böbreklerden sodyum ve suyun tutulması, idrarla potasyum atılımının artması", "isCorrect": True, "explanation": "Doğru cevap B'dir: Aldosteron distal tübülden sodyum ve suyu geri emerken potasyum ve hidrojeni idrara salgılar."},
                    {"key": "C", "text": "Tüm böbrek fonksiyonlarının tamamen normale dönmesi", "isCorrect": False, "explanation": "Yetmezlik tablosu derinleşir."},
                    {"key": "D", "text": "Kanda kalsiyumun sıfıra inmesi", "isCorrect": False, "explanation": "Kalsiyum homeostazı parathormonla ilişkilidir."}
                ]
            )
        ]
    })

    return slides
