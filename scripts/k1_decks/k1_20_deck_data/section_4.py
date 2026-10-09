# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_4_slides():
    slides = []

    # Slide 31
    slides.append({
        "id": "k1-20-s31",
        "title": "Pıhtılaşmanın Sınırlandırılması: Seyreltme ve Lokalizasyon",
        "content": "Bir damar yaralandığında pıhtılaşma kaskadı muazzam bir amplifikasyon potansiyeline sahiptir; tek bir aktif enzim binlerce molekülü aktive edebilir. Kontrol mekanizmaları olmasaydı küçük bir kesi tüm vücut damarlarının pıhtıyla dolmasına yol açardı (Sınav Spotu):\n\n- **1. Seyreltme (Wash-out Etkisi):**\n  - Yaralanma bölgesinden geçen kan akımı, aktive olan pıhtılaşma faktörlerini hızla sürükleyerek ortamdan uzaklaştırır ve seyreltir.\n  - Dolaşıma karışan aktif faktörler karaciğer kupffer hücreleri tarafından hızla fagositozla temizlenir.\n- **2. Membran Bağımlılığı (Lokalizasyon):**\n  - Enzim-kofaktör kompleksleri yalnızca aktive trombositlerin dışa dönmüş negatif yüklü fosfatidilserin yüzeyinde çalışabilir.\n  - Sağlam komşu endotel üzerinde bu negatif platform bulunmadığı için pıhtılaşma hasarlı bölge dışına yayılamaz.\n- **3. Endotel Kaynaklı İnhibitörler:** Sağlam endotel hücreleri sürekli olarak güçlü antikoagülan moleküller (trombomodulin, antitrombin, TFPI) eksprese ederek pıhtının önünü keser.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Kontrolsüz Pıhtılaşma vs Sınırlandırılmış Hemostaz",
                "Kontrolsüz Pıhtılaşma (Patolojik)",
                "Pıhtılaşma faktörleri hasar bölgesini aşar; tüm damar ağacına yayılarak masif tromboz yaratır.",
                "Sınırlandırılmış Hemostaz (Fizyolojik)",
                "Seyreltme, fosfolipid sınırlaması ve endotel antikoagülanları sayesinde pıhtı yalnız hasarlı bölgede kalır."
            ),
            make_cloze(
                "Hasar bölgesinde oluşan aktif pıhtılaşma faktörlerinin komşu sağlam dokulara yayılmasını engelleyen en temel fiziksel faktörlerden biri kan akımı ile faktörlerin seyreltilmesi etkisidir.",
                "seyreltilmesi",
                "Akan kanın aktif enzimleri hasar bölgesinden uzaklaştırıp konsantrasyonunu düşürme mekanizması"
            )
        ]
    })

    # Slide 32
    slides.append({
        "id": "k1-20-s32",
        "title": "Trombomodulin ve EPCR: Trombinin Yön Değiştirmesi",
        "content": "Pıhtılaşmayı başlatan ana faktör olan Trombin, sağlam damar duvarına ulaştığında kendi kendini durduran bir moleküler tuzağa düşer (Sınav Spotu):\n\n- **Trombomodulin Reseptörü:**\n  - Sağlam endotel hücrelerinin zarına gömülü bir transmembran glikoproteindir.\n  - Dolaşan trombin için son derece yüksek afiniteli bir 'tuzak' reseptördür.\n- **Konformasyonel Dönüşüm:**\n  - Trombin trombomoduline bağlandığı anda aktif bölgesinin şekli değişir.\n  - Fibrinojeni kesme, Faktör V ve VIII'i aktive etme ve trombositleri uyarma yeteneğini **tamamen kaybeder** (prokoagülan özelliği sıfırlanır).\n- **Protein C Aktivasyonu:**\n  - Trombomodulin-trombin kompleksi, endoteldeki **EPCR (Endotel Protein C Reseptörü)** tarafından sunulan inaktif **Protein C** molekülünü enzimatik olarak parçalayarak **Aktive Protein C (APC)** haline getirir.\n- **Paradoks:** Trombin, kendi celladını (Aktive Protein C) bizzat kendisi üreterek pıhtılaşmayı durduran anahtara dönüşür.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Trombomodulin ve Protein C Aktivasyon Kaskadı",
                [
                    "1. Trombin Göçü: Pıhtılaşan kandan serbest trombin sağlam endotele ulaşır.",
                    "2. Trombomoduline Bağlanma: Endotel yüzeyindeki trombomodulin trombin ile birleşir.",
                    "3. Prokoagülan Kayıp: Trombin fibrinojen kesme ve trombosit uyarma yeteneğini yitirir.",
                    "4. EPCR Sunumu: Endotel Protein C reseptörü inaktif Protein C'yi komplekse sunar.",
                    "5. Aktive Protein C (APC): Kompleks Protein C'yi parçalayarak aktif antikoagülana çevirir."
                ]
            ),
            make_cloze(
                "Sağlam endotel yüzeyinde trombine bağlanarak onun pıhtılaştırıcı etkisini yok eden ve Protein C'yi aktive eden transmembran reseptöre trombomodulin adı verilir.",
                "trombomodulin",
                "Trombini antikoagülan bir enzime dönüştüren endotelyal reseptör"
            )
        ]
    })

    # Slide 33
    slides.append({
        "id": "k1-20-s33",
        "title": "Aktive Protein C ve Protein S: Faktör Va ve VIIIa İnaktivasyonu",
        "content": "Aktive Protein C (APC), koagülasyon kaskadının en güçlü iki kofaktörünü parçalayarak pıhtılaşma motorunu durdurur (Sınav Spotu):\n\n- **Protein S Kofaktörlüğü:**\n  - Aktive Protein C (APC), serin proteaz aktivitesini gösterebilmek için plazmadaki bir diğer K vitamini bağımlı protein olan **Protein S** kofaktörüne ihtiyaç duyar.\n  - APC ve Protein S trombosit zarına birlikte oturur.\n- **Hedef Moleküller: Faktör Va ve Faktör VIIIa:**\n  - APC-Protein S kompleksi koagülasyon kaskadının iki kilit amplifikatör kofaktörünü hedefler:\n    1. **Faktör Va'yı parçalar:** Protrombinaz kompleksini yıkarak trombin üretimini durdurur.\n    2. **Faktör VIIIa'yı parçalar:** Tenaz kompleksini yıkarak Faktör X aktivasyonunu durdurur.\n- **Klinik Önem:**\n  - Protein C veya Protein S eksikliği olan bireylerde kaskad durdurulamaz; tekrarlayan venöz trombozlar ve pulmoner emboli görülür.\n  - Ayrıca bu hastalarda Varfarin tedavisi başlandığında geçici hiperkoagülabiliteye bağlı **Varfarin Nekrozu** gelişebilir.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Molekül", "K Vitamini Bağımlılığı", "Görevi", "Eksikliğinde Risk"],
                [
                    ["Protein C", "Evet (Gla içerir)", "Trombomodulinle aktive olur, Va ve VIIIa'yı parçalar", "Ağır venöz tromboz, neonatal purpura fulminans"],
                    ["Protein S", "Evet (Gla içerir)", "Aktive Protein C için zorunlu plazma kofaktörü", "Tekrarlayan derin ven trombozu (DVT)"],
                    ["Faktör Va ve VIIIa", "Hayır", "Kaskadın hızlandırıcı kofaktörleri", "Eksikliğinde kanama (Hemofili), parçalanamazsa tromboz"]
                ]
            ),
            make_quiz(
                "Aktive Protein C (APC) plazmada Protein S kofaktörlüğü ile koagülasyon kaskadındaki hangi iki kritik kofaktörü proteolitik olarak parçalayarak inaktive eder?",
                [
                    {"key": "A", "text": "Faktör Va ve Faktör VIIIa", "isCorrect": True, "explanation": "Doğru cevap A'dır: Aktive Protein C (APC), kaskadın iki ana akseleratör kofaktörü olan Faktör Va ve Faktör VIIIa'yı parçalayarak pıhtılaşmayı güçlü şekilde durdurur."},
                    {"key": "B", "text": "Faktör II ve Faktör X", "isCorrect": False, "explanation": "Faktör II ve X serin proteazlardır, APC'nin primer hedefi kofaktörlerdir (Va ve VIIIa)."},
                    {"key": "C", "text": "Faktör VII ve Faktör XII", "isCorrect": False, "explanation": "Bu faktörler APC tarafından parçalanmaz."},
                    {"key": "D", "text": "Fibrinojen ve Faktör XIII", "isCorrect": False, "explanation": "Fibrinojen plazmin tarafından parçalanır."}
                ]
            )
        ]
    })

    # Slide 34
    slides.append({
        "id": "k1-20-s34",
        "title": "Heparin Benzeri Moleküller ve Antitrombin III (ATIII)",
        "content": "Dolaşımdaki aktif serin proteazları doğrudan intihar substratı gibi yakalayan en güçlü plazma inhibitörü **Antitrombin III'tür (ATIII)** (Sınav Spotu):\n\n- **Serpin Ailesi (Serin Proteaz İnhibitörü):** Karaciğerde üretilen ATIII, kanda serbest dolaşır ve aktif proteazların merkezine bağlanarak onları geri dönüşümsüz olarak kilitler.\n- **Hedefleri:** Başta **Trombin (Faktör IIa)** ve **Faktör Xa** olmak üzere; Faktör IXa, XIa ve XIIa'yı da nötralize eder.\n- **Endotel Heparan Sülfatı ile Aktivasyon:**\n  - Plazmada serbest ATIII oldukça yavaş çalışır.\n  - Ancak sağlam endotel hücrelerinin yüzeyinde bulunan **heparin benzeri proteoglikanlar (heparan sülfat)** ile birleştiğinde ATIII'ün konformasyonu dramatik olarak değişir.\n  - Bu bağlanma ATIII'ün trombin ve Faktör Xa'yı inaktive etme hızını **yaklaşık 1000 ila 2000 kat artırır**.\n- **Farmakolojik Yansıma:** Klinik tedavide kullanılan **standart heparin ve düşük molekül ağırlıklı heparinler (DMAH)** bu doğal fizyolojik mekanizmayı taklit ederek ATIII'ü aktive ederler.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Serbest Antitrombin III vs Heparinle Birleşmiş ATIII",
                "Serbest ATIII (Yavaş İnhibitör)",
                "Plazmada dolaşırken trombin ve Xa'yı çok yavaş hızda inaktive eder.",
                "Heparin / Heparan Sülfatlı ATIII (1000 Kat Hızlı)",
                "Konformasyonel değişimle trombin ve Faktör Xa'yı anında kilitler; pıhtılaşmayı hemen durdurur."
            ),
            make_cloze(
                "Endotel yüzeyindeki heparan sülfat moleküllerine bağlanarak trombin ve Faktör Xa'yı bin kat daha hızlı inaktive eden plazma proteini Antitrombin III proteinidir.",
                "Antitrombin III",
                "Heparin ile aktive olarak pıhtılaşma faktörlerini kovalayan temel serpin inhibitörü"
            )
        ]
    })

    # Slide 35
    slides.append({
        "id": "k1-20-s35",
        "title": "Doku Faktörü Yolu İnhibitörü (TFPI): Başlangıç Freni",
        "content": "Kaskadın en erken basamağını denetleyen endotelyal kontrol mekanizması **TFPI (Tissue Factor Pathway Inhibitor)** proteinidir (Sınav Spotu):\n\n- **Sentez ve Depolanma:** Büyük oranda mikrovasküler endotel hücreleri tarafından sentezlenir; bir kısmı endotel yüzeyindeki proteoglikanlara bağlı, bir kısmı plazmada lipoproteinlere bağlı, bir kısmı da trombositlerde depolanır.\n- **İki Basamaklı İnhibisyon Mekanizması:**\n  1. İlk olarak dolaşımdaki aktif **Faktör Xa'ya** doğrudan bağlanır ve onu nötralize eder.\n  2. Ardından oluşan bu [TFPI - Xa] kompleksi, hasar bölgesindeki **Doku Faktörü - Faktör VIIa (TF-VIIa)** kompleksine bağlanarak kaskadı başladığı ilk kapıda tamamen kilitler.\n- **Klinik ve Sınav Önemi (Çıkmış Soru):**\n  - TFPI doğrudan fibrini eritmez; fibrinolitik DEĞİLDİR.\n  - TFPI bir **antikoagülandır** ve doku faktörü-Faktör VIIa kompleksini engelleyerek yeni trombin oluşumunu baştan sınırlar.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "TFPI İnhibisyon Mekanizması",
                [
                    "1. Faktör Xa Yakalama: TFPI önce aktifleşen Faktör Xa'ya bağlanır.",
                    "2. Dörtlü Kompleks: [TFPI-Xa] kompleksi hasarlı yüzeydeki TF-VIIa'ya kilitlenir.",
                    "3. Giriş Kapısının Kapanması: Doku faktörü yolu tamamen bloke edilir.",
                    "4. Yeni Faktör Üretiminin Durması: İlave Faktör IX ve X aktivasyonu engellenir."
                ]
            ),
            make_quiz(
                "Aşağıdaki moleküllerden hangisi doku faktörü-faktör VIIa kompleksini inhibe ederek ekstrinsik yolu durduran bir antikoagülandır ancak FİBRİNOLİTİK ETKİSİ YOKTUR?",
                [
                    {"key": "A", "text": "Doku Faktörü Yolak İnhibitörü (TFPI)", "isCorrect": True, "explanation": "Doğru cevap A'dır: TFPI koagülasyonu başlatan TF-VIIa kompleksini inhibe eden bir antikoagülandır; fibrinolitik (pıhtı eritici) etkisi yoktur."},
                    {"key": "B", "text": "Plazmin", "isCorrect": False, "explanation": "Plazmin asıl fibrinolitik enzimdir."},
                    {"key": "C", "text": "Doku Plazminojen Aktivatörü (t-PA)", "isCorrect": False, "explanation": "t-PA fibrinolitik sistemi aktive eder."},
                    {"key": "D", "text": "Ürokinaz", "isCorrect": False, "explanation": "Ürokinaz fibrinolitik bir aktivatördür."}
                ]
            )
        ]
    })

    # Slide 36
    slides.append({
        "id": "k1-20-s36",
        "title": "Fibrinolitik Sistem: Plazminojenin Plazmine Aktivasyonu",
        "content": "Pıhtı oluştuktan ve damar hasarı tamir edildikten sonra pıhtı kitlesinin eritilerek damar lümeninin yeniden açılması **Fibrinoliz** süreciyle yürütülür (Sınav Spotu):\n\n- **Merkezi Enzim: Plazmin:**\n  - Fibrinolitik sistemin asıl yürütücüsü olan **Plazmin**, karaciğer kökenli inaktif bir proenzim olan **Plazminojenin** proteolitik olarak parçalanmasıyla oluşur.\n  - Plazmin, fibrin ağını, fibrinojeni ve Faktör V ile VIII'i sindiren güçlü bir serin proteazdır.\n- **İki Temel Fizyolojik Aktivatör:**\n  1. **t-PA (Doku Plazminojen Aktivatörü):** Endotel hücreleri tarafından sentezlenir. En kritik özelliği **fibrine bağlandığında aktivitesinin yüzlerce kat artmasıdır**; bu sayede serbest kanda değil yalnızca pıhtı üzerinde plazmin üretir.\n  2. **Ürokinaz (u-PA):** Plazmada ve idrarda bulunur; doku invazyonunda ve hücre dışı matriks yıkımında görev alır.\n- **Terapötik Tromboliz:** Akut miyokard enfarktüsü veya iskemik inmede ilk saatlerde verilen rekombinant t-PA (Alteplaz), tıkacı eriterek dokuyu kurtarır.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "İnaktif Plazminojen vs Aktif Plazmin",
                "Plazminojen (İnaktif Proenzim)",
                "Karaciğerde üretilir; plazmada dolaşır ve pıhtılaşma sırasında fibrin ağı içine hapsolur.",
                "Plazmin (Aktif Pıhtı Eritici)",
                "t-PA ile aktive olur; çözünmeyen fibrin polimerlerini parçalayarak çözünür yıkım ürünlerine çevirir."
            ),
            make_cloze(
                "Fibrinolitik sistemde çözünmeyen fibrin liflerini sindirerek pıhtıyı eriten temel proteolitik enzim plazmin enzimidir.",
                "plazmin",
                "Plazminojenin t-PA ile parçalanması sonucu oluşan aktif fibrinolitik serin proteaz"
            )
        ]
    })

    # Slide 37
    slides.append({
        "id": "k1-20-s37",
        "title": "Fibrin Yıkım Ürünleri ve D-Dimer: Çapraz Bağlı Pıhtı İmzası",
        "content": "Plazminin fibrini eritmesi sonucunda kana karışan fragmanlar klinikte trombozun en değerli laboratuvar göstergeleridir (Sınav Spotu):\n\n- **Fibrin Yıkım Ürünleri (FDP):**\n  - Plazmin hem fibrinojeni hem de olgun fibrini yıkar; X, Y, D ve E parçaları oluşur (genel FDP).\n  - Yüksek FDP düzeyleri trombosit agregasyonunu ve fibrin polimerizasyonunu bozar (doğal antikoagülan etki).\n- **D-Dimer: Olgun Çapraz Bağlı Pıhtının Spesifik İmzası:**\n  - Fibrin monomerleri Faktör XIIIa tarafından kovalent olarak çapraz bağlandığında komşu iki D domeni kovalent bağla birleşir.\n  - Plazmin bu ağı yıktığında geriye bu kovalent bağlı iki D parçasını içeren **D-Dimer (D-D fragmanı)** kalır.\n  - Fibrinojenin veya çapraz bağsız erken fibrinin yıkımında D-Dimer oluşamaz; **D-Dimer yalnızca vücutta önceden oluşmuş ve Faktör XIIIa ile stabilize edilmiş gerçek bir pıhtının varlığını kanıtlar**.\n- **Klinik Kullanım:** DVT ve Pulmoner Emboli şüphesinde negatif prediktif değeri çok yüksektir (D-Dimer negatifse tromboz ekarte edilir).",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "D-Dimer Oluşum Basamakları",
                [
                    "1. Fibrin Ağı: Trombin fibrinojeni keserek fibrin polimerlerini oluşturur.",
                    "2. Faktör XIIIa Çapraz Bağı: Komşu D domenleri kovalent bağla birbirine yapışır.",
                    "3. Plazmin Aktivasyonu: t-PA ile aktive olan plazmin fibrin liflerini keser.",
                    "4. D-Dimer Salınımı: Kovalent bağlı iki D parçası (D-Dimer) dolaşıma geçer.",
                    "5. Tanısal Değer: Plazmada D-Dimer yüksekliği aktif tromboz ve lizisi gösterir."
                ]
            ),
            make_quiz(
                "Klinikte derin ven trombozu veya pulmoner emboli dışlamasında kullanılan ve yalnızca Faktör XIIIa ile çapraz bağlanmış olgun fibrinin plazmin tarafından eritildiğini kanıtlayan spesifik belirteç hangisidir?",
                [
                    {"key": "A", "text": "D-Dimer", "isCorrect": True, "explanation": "Doğru cevap A'dır: D-Dimer, Faktör XIIIa tarafından çapraz bağlanmış fibrinin plazminle yıkılması sonucu açığa çıkan spesifik üründür."},
                    {"key": "B", "text": "Fibrinopeptid A", "isCorrect": False, "explanation": "Fibrinopeptid A trombin kesiminde ayrılır, lizis ürünü değildir."},
                    {"key": "C", "text": "Protrombin fragmanı 1+2", "isCorrect": False, "explanation": "Trombin oluşumunu gösterir."},
                    {"key": "D", "text": "Trombosit Faktör 4", "isCorrect": False, "explanation": "Trombosit degranülasyonunu gösterir."}
                ]
            )
        ]
    })

    # Slide 38
    slides.append({
        "id": "k1-20-s38",
        "title": "Fibrinoliz İnhibitörleri: Alfa-2-Antiplazmin ve PAI-1",
        "content": "Fibrinolitik sistemin de tıpkı pıhtılaşma gibi kontrolsüz kanamalara yol açmaması için güçlü inhibitörleri vardır (Sınav Spotu):\n\n- **1. Plazminojen Aktivatör İnhibitörü-1 (PAI-1):**\n  - Endotel hücreleri, vasküler düz kas ve adipositler (yağ dokusu) tarafından sentezlenir.\n  - Doğrudan **t-PA ve ürokinazı bağlayarak inaktive eder**; böylece plazmin oluşumunu baştan engeller.\n  - **Tromboza Eğilim:** Sitokinler (TNF, IL-1), obezite, insülin direnci ve endotel hasarında PAI-1 salgısı dramatik artar; bu durum fibrinolizi baskılayarak **tromboz riskini katlar**.\n- **2. Alfa-2-Antiplazmin (α2-Antiplazmin):**\n  - Karaciğerde sentezlenen ve plazmada serbest dolaşan temel plazmin inhibitörüdür.\n  - Pıhtıdan kaçarak serbest dolaşıma geçen **plazmini 1:1 oranında hızla bağlar ve nötralize eder**.\n  - Bu sayede serbest plazminin dolaşımdaki fibrinojeni ve diğer pıhtılaşma faktörlerini eriterek sistemik bir kanama felaketi yaratması önlenir.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Fibrinoliz İnhibitörü", "Sentezlendiği Yer", "Hedeflediği Molekül", "Klinik Yansıması"],
                [
                    ["PAI-1", "Endotel, düz kas, yağ dokusu", "t-PA ve ürokinazı bloke eder", "Yüksekliğinde pıhtı eriyemez, tromboz riski artar"],
                    ["α2-Antiplazmin", "Karaciğer parankimi", "Serbest plazmini kilitler", "Eksikliğinde kontrolsüz sistemik hiperfibrinoliz ve kanama"],
                    ["TAFI", "Karaciğer", "Fibrin üzerindeki lizin uçlarını keser", "Plazminojenin fibrine bağlanmasını önler"]
                ]
            ),
            make_cloze(
                "Endotel ve yağ dokusu tarafından salgılanarak doku plazminojen aktivatörünü (t-PA) bloke eden ve fibrinolizi baskılayan temel inhibitör PAI-1 inhibitörüdür.",
                "PAI-1",
                "Plazminojen aktivatör inhibitörü-1 kısaltması"
            )
        ]
    })

    # Slide 39 - CHECKPOINT 4
    slides.append({
        "id": "k1-20-s39",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 4] Antikoagülan Sistem ve Fibrinoliz",
        "content": "Bu checkpointte pıhtılaşmayı sınırlandıran antikoagülan ve fibrinolitik mekanizmaları özetliyoruz:\n\n- **Trombomodulin:** Endotel reseptörüdür; trombinin prokoagülan yönünü sıfırlayıp **Protein C'yi aktive eder**.\n- **Aktive Protein C (APC) ve Protein S:** Kaskadın iki kilit hızlandırıcısı olan **Faktör Va ve Faktör VIIIa'yı parçalayarak** kaskadı durdurur.\n- **Antitrombin III (ATIII):** Endoteldeki heparin benzeri moleküllerle (heparan sülfat) aktive olur; aktivitesi 1000 kat artarak **Trombin ve Faktör Xa'yı kilitler**.\n- **TFPI:** Önce Xa'yı bağlar, ardından **TF-VIIa kompleksini bloke eder**; antikoagülandır, fibrinolitik değildir.\n- **Fibrinoliz (Plazmin):** Plazminojen **t-PA** ile parçalanıp plazmin olur; çözünmeyen fibrini sindirir; t-PA fibrine bağlıyken en aktiftir.\n- **D-Dimer:** Yalnızca **Faktör XIIIa ile çapraz bağlanmış olgun fibrinin** plazminle yıkılmasıyla oluşur; DVT/PTE dışlamasında kullanılır.\n- **İnhibitörler:** **PAI-1** t-PA'yı bloke eder (tromboza eğilim); **α2-antiplazmin** serbest plazmini nötralize eder.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Mekanizma", "Anahtar Molekül", "Hedef / Fonksiyon", "Klinik Bağlantı"],
                [
                    ["Protein C Yolu", "APC + Protein S", "Faktör Va ve VIIIa inaktivasyonu", "Eksiklikte DVT ve Varfarin nekrozu"],
                    ["Antitrombin Yolu", "ATIII + Heparan sülfat", "Trombin ve Faktör Xa blokajı", "Heparin tedavisinin biyolojik temeli"],
                    ["TFPI Yolu", "TFPI", "TF-VIIa kompleksi inhibisyonu", "Erken kaskad kapısını kapatma"],
                    ["Fibrinolitik Yol", "t-PA $\\to$ Plazmin", "Fibrin ağını eritme $\\to$ D-Dimer", "Akut MI/inmede trombolitik tedavi"],
                    ["Fibrinoliz Freni", "PAI-1 ve α2-antiplazmin", "t-PA ve plazmini durdurma", "İnflamasyonda tromboz artışı"]
                ]
            ),
            make_chain(
                "Doğal Antikoagülan ve Fibrinoliz Akışı",
                [
                    "1. Trombin Bağlantısı: Trombomodulin trombin ile Protein C'yi aktive eder.",
                    "2. Kofaktör Yıkımı: APC ve Protein S Faktör Va ve VIIIa'yı parçalar.",
                    "3. Serpin Kilidi: Heparan sülfat ile ATIII trombin ve Xa'yı nötralize eder.",
                    "4. Plazmin Aktivasyonu: t-PA fibrine bağlanarak plazminojeni plazmine çevirir.",
                    "5. Pıhtı Erimesi: Plazmin fibrini eritir ve D-Dimer fragmanları serbest kalır."
                ]
            )
        ]
    })

    # Slide 40
    slides.append({
        "id": "k1-20-s40",
        "title": "Bölüm Özeti: Fibrinolizden Virchow Üçlüsüne Geçiş",
        "content": "Bölüm 4 boyunca pıhtının aşırı büyümesini engelleyen antikoagülan kalkanları ve fibrinolitik eritme mekanizmalarını inceledik:\n\n- **Özet:** Sağlam endotel PGI2, NO, trombomodulin, heparan sülfat ve t-PA ile antikoagülan ve fibrinolitik bir bariyer kurar.\n- **Sonraki Bölüm (Bölüm 5):** Bu dengenin bozulup damar içinde trombozun tetiklenmesini açıklayan tıp tarihinin en ünlü teorisi olan **Virchow Üçlüsünü (Endotel Hasarı, Anormal Kan Akımı ve Hiperkoagülabilite)** ve endotel aktivasyonunun moleküler basamaklarını ele alacağız.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_recall(
                "Endotel hücreleri tarafından salgılanarak t-PA'yı bloke eden ve obezite ile inflamasyonda artarak tromboza zemin hazırlayan inhibitör hangisidir?",
                "PAI-1 (Plazminojen Aktivatör İnhibitörü-1)",
                "Fibrinolizi baştan durduran endotel kaynaklı inhibitör protein"
            ),
            make_quiz(
                "Aşağıdaki moleküllerden hangisi sağlam endotel yüzeyinde K vitamini bağımlı Protein C'yi aktive ederek Faktör Va ve VIIIa'nın parçalanmasını sağlar?",
                [
                    {"key": "A", "text": "Trombomodulin", "isCorrect": True, "explanation": "Doğru cevap A'dır: Trombomodulin trombini bağlayarak Protein C'yi aktive eder ve antikoagülan etkiyi başlatır."},
                    {"key": "B", "text": "Doku Faktörü", "isCorrect": False, "explanation": "Doku faktörü prokoagülandır."},
                    {"key": "C", "text": "Fibrinojen", "isCorrect": False, "explanation": "Fibrinojen pıhtının hammaddesidir."},
                    {"key": "D", "text": "Faktör XIII", "isCorrect": False, "explanation": "Faktör XIII pıhtıyı stabilize eder."}
                ]
            )
        ]
    })

    return slides
