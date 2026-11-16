# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_6_slides():
    slides = []

    # Slide 51
    slides.append({
        "id": "k1-12-s51",
        "title": "Kompleman Sistemine Giriş: Plazma Kaynaklı Proteolitik Kaskad",
        "content": "Plazma kaynaklı mediyatör sistemlerinin en eskisi ve en güçlüsü olan **Kompleman Sistemi**, humoral bağışıklığın ve konak savunmasının temel taşını oluşturur. Başlıca **karaciğer** tarafından sentezlenip plazmaya verilen ve toplam plazma globulinlerinin yaklaşık %10'unu oluşturan 30'dan fazla çözünebilir protein ve membran reseptöründen meydana gelir. Dolaşımda C1'den C9'a kadar numaralandırılmış zimojen (inaktif enzim öncülü) formda serbestçe dolaşırlar. Bir enfeksiyon veya doku hasarı ile tetiklendiklerinde, birbirini ardı ardına proteolitik olarak parçalayan 'enzimatik bir amplifikasyon kaskadı' şeklinde çalışırlar. Sistem; patojenlerin opsonizasyonu (yutulabilir hale getirilmesi), kemotaksi ile lökosit toplanması, mast hücrelerinden histamin salınımı ve patojen zarının doğrudan parçalanması (membran lizisi) gibi hayati görevleri yerine getirir.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_cloze(
                "Kompleman sistemi proteinleri baslıca karaciğer tarafından sentezlenir ve kanda inaktif zimojenler olarak dolasır.",
                "karaciğer",
                "Kompleman proteinlerinin ana sentez fabrikası olan organ"
            ),
            make_quiz(
                "Kompleman sisteminin genel özellikleri ve biyolojik aktivasyonuyla ilgili hangisi DOĞRUDUR?",
                [
                    {"key": "A", "text": "Dolaşımda inaktif prekürsörler olarak bulunur ve basamaklı proteolitik kaskadla aktive olurlar.", "explanation": "A seçeneği DOĞRUDUR: Karaciğerde zimojen olarak üretilirler ve proteoliz basamaklarıyla amplifiye olurlar."},
                    {"key": "B", "text": "Yalnızca kemik iliğinde depolanıp granüllerle dışarı atılırlar.", "explanation": "B seçeneği yanlıştır: Plazma proteinleridir."},
                    {"key": "C", "text": "Bakterileri besleyerek onların çoğalmasını sağlarlar.", "explanation": "C seçeneği anlamsızdır: Konak savunma sistemidir."},
                    {"key": "D", "text": "Hiçbir reseptör içermeyen tek tip bir nükleik asit zinciridir.", "explanation": "D seçeneği yanlıştır: Protein ve reseptör kompleksidir."},
                    {"key": "E", "text": "Yalnızca böbrek tübül lümeninde aktifleşebilirler.", "explanation": "E seçeneği yanlıştır: Sistemik vasküler alanda aktiftirler."}
                ],
                "A"
            )
        ]
    })

    # Slide 52
    slides.append({
        "id": "k1-12-s52",
        "title": "Kompleman Aktivasyonunun 3 Ana Yolu: Tetikleyiciler ve Ayrım",
        "content": "Kompleman kaskadı farklı mikrobiyal ve immünolojik uyaranlar tarafından üç bağımsız başlangıç yolu üzerinden tetiklenebilir:\n\n1. **Klasik Yol:** Kazanılmış (adaptif) bağışıklık ile ilişkilidir. Hedef antijenlere bağlanmış spesifik **IgG (özellikle IgG1, IgG3) veya IgM** tipi antijen-antikor kompleksleri (bağışıklık kompleksleri) tarafından başlatılır.\n2. **Alternatif Yol:** Doğal (innate) bağışıklığın parçasıdır. Antikor varlığı gerektirmez. Doğrudan mikrobiyal yüzey molekülleri (Gram-negatif bakteri endotoksini / **LPS**, maya hücre duvarı zimosanı, parazit yüzeyleri) ve plazmadaki spontan C3 hidrolizi ('tickover') ile tetiklenir.\n3. **Lektin Yolu:** Antikordan bağımsızdır. Plazmada dolaşan **Mannoz Bağlayıcı Lektin (MBL)** proteininin mikrop yüzeyindeki terminal mannoz ve glikoz kalıntılarına bağlanmasıyla devreye girer.\n\nHer üç yol da farklı mekanizmalarla başlasa da, nihayetinde tek bir ortak kavşakta birleşir: **C3 Konvertaz enziminin oluşturulması**.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Aktivasyon Yolu", "Primer Tetikleyici Faktör", "Bağışıklık Tipi"],
                [
                    [
                        {"text": "Klasik Yol", "isMasked": False, "hint": ""},
                        {"text": "Antijen-antikor kompleksleri (IgG, IgM)", "isMasked": True, "hint": "İmmünoglobülin bağımlı yol"},
                        {"text": "Kazanılmış (Adaptif) Bağışıklık", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Alternatif Yol", "isMasked": False, "hint": ""},
                        {"text": "Bakteriyel LPS, polisakkaritler ve zimosan", "isMasked": True, "hint": "Doğrudan mikrop yüzey teması"},
                        {"text": "Doğal (İnnate) Bağışıklık", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Lektin Yolu", "isMasked": False, "hint": ""},
                        {"text": "MBL'nin mikrobiyal mannoz şekerlerine bağlanması", "isMasked": True, "hint": "Karbonhidrat tanıyan çözünebilir lektin"},
                        {"text": "Doğal (İnnate) Bağışıklık", "isMasked": False, "hint": ""}
                    ]
                ]
            ),
            make_cloze(
                "Kompleman sisteminin klasik aktivasyon yolu antijenlere bağlanmış IgG ve IgM tipi antikorlar tarafından tetiklenir.",
                "IgG ve IgM",
                "Klasik yolu başlatan iki temel immünoglobülin sınıfı"
            )
        ]
    })

    # Slide 53
    slides.append({
        "id": "k1-12-s53",
        "title": "Klasik Yol Kaskadı: C1 Kompleksinden C4b2a Konvertazına",
        "content": "Klasik yol, bir lale demetini andıran devasa **C1 kompleksi** (C1q, iki C1r ve iki C1s alt birimi) ile başlar:\n\n1. C1q başlıkları, antijene bağlanarak konformasyonel değişime uğramış en az iki IgG molekülünün Fc bölgesine veya tek bir pentamerik IgM molekülüne tutunur.\n2. C1q'nun bağlanması serin proteaz olan C1r'yi, o da C1s'i aktif enzim formuna dönüştürür.\n3. Aktif C1s enzimi dolaşımdaki C4 proteinini C4a ve **C4b'ye**; C2 proteinini ise C2b ve **C2a'ya** parçalar.\n4. C4b ve C2a mikrop yüzeyinde bir araya gelerek klasik yolun **C3 Konvertaz enzim kompleksini (C4b2a)** oluşturur.\n\nBu membran bağlantılı C4b2a enzimi, kaskadın kalbi olan C3 moleküllerini parçalayarak amplifikasyonu katlar.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Klasik Kompleman Yolu Aktivasyon Zinciri",
                [
                    "1. İmmün Kompleks Tanıma: C1q'nun antijene bağlı IgG veya IgM'ye tutunması",
                    "2. Proteaz Aktivasyonu: C1r ve C1s serin proteazlarının aktifleşmesi",
                    "3. C4 ve C2 Parçalanması: C1s'in C4 ve C2'yi bölerek C4b ve C2a üretmesi",
                    "4. C3 Konvertaz Oluşumu: C4b2a kompleksinin mikrop zarına kenetlenmesi"
                ]
            ),
            make_recall(
                "Klasik kompleman aktivasyon yolunda C3 molekülünü parçalayan C3 konvertaz enzim kompleksi hangi alt birimlerden oluşur?",
                "C4b2a kompleksidir.",
                "C4b ve C2a'nın oluşturduğu klasik enzim kompleksi"
            )
        ]
    })

    # Slide 54
    slides.append({
        "id": "k1-12-s54",
        "title": "Alternatif Yol: Spontan Tickover, Faktör B, Faktör D ve C3bBb",
        "content": "Alternatif yol, antikora hiç ihtiyaç duymayan ve mikroplarla ilk temas anında saniyeler içinde patlayan en ilkel konak savunmasıdır:\n\n- **Spontan Tickover (Gıdıklanma):** Plazmadaki C3 molekülünün içindeki reaktif tiyoester bağı fizyolojik koşullarda çok yavaş bir hızla su molekülleriyle spontan hidrolize uğrar ve C3(H2O) oluşur.\n- **Faktör B ve Faktör D Katılımı:** C3(H2O) veya mikrop zarına bağlanan az miktardaki C3b, plazma proteini olan **Faktör B'ye** bağlanır. Dolaşımdaki aktif serin proteaz **Faktör D**, bu kompleksteki Faktör B'yi keserek Ba parçasını uzaklaştırır ve aktif Bb parçasını bırakır.\n- **Alternatif C3 Konvertaz (C3bBb):** Mikrop zarına kovalent tutunan C3b ve Bb, alternatif yolun C3 konvertazını (**C3bBb**) kurar.\n- **Properdin (Faktör P):** C3bBb kompleksi normalde hızla dağılır; ancak plazma proteini **Properdin (Faktör P)** bu komplekse bağlanarak stabilitesini 10 kat artırır ve kaskadı muazzam bir pozitif geri bildirim döngüsüne sokar.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Klasik ve Alternatif C3 Konvertaz Karşılaştırması",
                "Klasik Yol C3 Konvertazı (C4b2a)",
                "Antijen-antikor kompleksiyle uyarılır; C4b ve C2a alt birimlerinden meydana gelir.",
                "Alternatif Yol C3 Konvertazı (C3bBb)",
                "Doğrudan mikrop zarı ve LPS ile tetiklenir; C3b ve Faktör Bb'den oluşur, Properdin ile stabilize edilir."
            ),
            make_recall(
                "Alternatif kompleman yolunda C3bBb konvertaz enzim kompleksine bağlanarak stabilitesini ve ömrünü artıran plazma proteini hangisidir?",
                "Properdindir (Faktör P).",
                "Alternatif yolu stabilize eden tek pozitif düzenleyici protein"
            )
        ]
    })

    # Slide 55
    slides.append({
        "id": "k1-12-s55",
        "title": "Lektin Yolu: Mannoz Bağlayıcı Lektin ve MASP Proteazları",
        "content": "Lektin yolu yapı ve fonksiyon olarak klasik yola çok benzer; ancak antikor yerine çözünebilir bir pattern recognition reseptörü (PRR) kullanır:\n\n1. **Mannoz Bağlayıcı Lektin (MBL):** Kolektin protein ailesinin üyesidir; yapay olarak C1q'ya benzer çok başlı bir yapı sergiler. Memeli hücreleri mannoz şekerlerini sialik asit ile maskelerken; mantarlar, bakteriler ve bazı virüsler yüzeylerinde terminal mannoz, fukoz ve N-asetilglukozamin şekerlerini açıkta taşırlar. MBL bu mikrobiyal şekerlere yüksek afiniteyle bağlanır.\n2. **MASP Aktivasyonu:** MBL'ye bağlı bulunan **MASP-1 ve MASP-2 (MBL-Associated Serine Proteases)** enzimleri C1r ve C1s gibi aktive olur.\n3. **Klasik Konvertaz Kurulumu:** Aktif MASP-2 enzimi, C4 ve C2 proteinlerini keserek tıpkı klasik yoldaki gibi **C4b2a (C3 Konvertaz)** enzimini kurar.\n\nMBL eksikliği özellikle bebeklerde ve küçük çocuklarda tekrarlayan ağır piyojenik enfeksiyonlara yol açar.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_cloze(
                "Lektin aktivasyon yolunda mikrop yüzeyindeki mannoz kalıntılarını tanıyan kolektin ailesi proteini mannoz bağlayıcı lektindir.",
                "mannoz bağlayıcı lektindir",
                "MBL kısaltmasının açık Türkçe karşılığı"
            ),
            make_quiz(
                "Kompleman lektin yolunda MBL'ye bağlı bulunan ve C4 ile C2'yi keserek klasik konvertazı kuran serin proteaz enzimi hangisidir?",
                [
                    {"key": "A", "text": "MASP-2 (MBL-ilişkili serin proteaz-2)", "explanation": "A seçeneği DOĞRUDUR: MASP-2 tıpkı C1s gibi C4 ve C2'yi keserek C4b2a'yı oluşturur."},
                    {"key": "B", "text": "Faktör D", "explanation": "B seçeneği yanlıştır: Alternatif yolda Faktör B'yi keser."},
                    {"key": "C", "text": "Fibrinaz (Faktör XIII)", "explanation": "C seçeneği yanlıştır: Pıhtılaşma faktörüdür."},
                    {"key": "D", "text": "Kallikrein", "explanation": "D seçeneği yanlıştır: Kinin sistemine aittir."},
                    {"key": "E", "text": "Protein C", "explanation": "E seçeneği yanlıştır: Antikoagülan proteindir."}
                ],
                "A"
            )
        ]
    })

    # Slide 56
    slides.append({
        "id": "k1-12-s56",
        "title": "Merkezi Kavşak: C3 Konvertaz ve C5 Konvertaz Kaskadı",
        "content": "Kompleman aktivasyonunun hangi yoldan başladığı önemsizdir; tüm yollar **C3 Konvertaz** basamağında kesişir. C3 plazmada en yüksek konsantrasyonda bulunan kompleman proteinidir (yaklaşık 1.2 mg/mL):\n\n1. **C3 Parçalanması:** C3 konvertaz enzimleri (C4b2a veya C3bBb) C3 molekülünü iki fonksiyonel parçaya böler:\n   - **C3a:** Küçük çözünebilir peptit; doku sıvısına difüze olarak **anafilatoksin** görevi yapar.\n   - **C3b:** Büyük aktif parça; içindeki tiyoester bağı açığa çıkar ve mikrop yüzeyindeki protein veya karbonhidratlara kovalent bağlanır (**opsonin**).\n2. **C5 Konvertaz Kurulumu:** Mikrop yüzeyinde biriken C3b moleküllerinden biri mevcut C3 konvertazına eklenir. Klasik yolda **C4b2a3b**, alternatif yolda ise **C3bBb3b** kompleksi oluşur; bu yeni enzim **C5 Konvertazdır**.\n3. **C5 Bölünmesi:** C5 konvertaz C5 molekülünü parçalar: Küçük **C5a (güçlü anafilatoksin ve kemoatraktan)** serbest kalırken, büyük **C5b** mikrop zarında kalarak Membran Atak Kompleksinin (MAC) montajını başlatır.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Merkezi Kompleman Amplifikasyon Zinciri",
                [
                    "1. C3 Konvertaz: Klasik (C4b2a) veya alternatif (C3bBb) enzimin kurulması",
                    "2. C3 Bölünmesi: C3a anafilatoksini ve C3b opsonininin devasa miktarda üretimi",
                    "3. C5 Konvertaz Geçişi: Enzime ek bir C3b katılarak C5 konvertaza evrilmesi",
                    "4. C5 Bölünmesi: C5a kemoatraktanı ve C5b terminal başlatıcısının açığa çıkması"
                ]
            ),
            make_recall(
                "Kompleman sisteminde plazmada en yüksek konsantrasyonda bulunan ve tüm aktivasyon yollarının kesiştiği merkezi protein hangisidir?",
                "C3 proteinidir.",
                "Sistemin niceliksel olarak en bol bulunan anahtar proteini"
            )
        ]
    })

    # Slide 57
    slides.append({
        "id": "k1-12-s57",
        "title": "Komplemanın Biyolojik Etkileri - I: Anafilatoksinler (C3a ve C5a)",
        "content": "Kompleman aktivasyonu sırasında açığa çıkan küçük çözünebilir parçalar olan **C3a ve C5a**, enflamatuar vasküler yanıtın en güçlü plazma tetikleyicileridir. Bu moleküllere sistemik düzeyde anafilaksi benzeri semptomlar üretebildikleri için **'Anafilatoksinler'** adı verilir (C4a da zayıf bir anafilatoksindir ancak C5a ve C3a çok daha potenttir):\n\n- **Mast Hücresi ve Bazofil Degranülasyonu:** C3a ve C5a, mast hücresi yüzeyindeki spesifik G-protein kenetli reseptörlerine (C3aR ve C5aR1) bağlanarak hücreyi saniyeler içinde degranüle eder. Mast hücrelerinden masif **histamin** salınır.\n- **Vasküler Permeabilite ve Vazodilatasyon:** Açığa çıkan histamin ve endotel üzerindeki doğrudan C5a etkileriyle arterioler vazodilatasyon ve postkapiller venüllerde endotel kasılması gelişir; dokuya yoğun eksüda ve plazma proteini sızar.\n- **Düz Kas Kasılması:** Bronş ve bağırsak düz kaslarında kasılmaya yol açarlar.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Anafilatoksinlerin Güç Karşılaştırması",
                "C5a Anafilatoksini",
                "En potent anafilatoksindir; hem masif histamin salar hem de lökositler için aşırı güçlü kemoatraktandır.",
                "C3a Anafilatoksini",
                "C5a'dan daha zayıftır; mast hücre degranülasyonu yapar fakat kemotaktik gücü C5a kadar yüksek değildir."
            ),
            make_cloze(
                "Mast hücrelerinden antikor bağımsız histamin salınımı yaparak vasküler geçirgenliği artıran kompleman parçalarına anafilatoksinler denir.",
                "anafilatoksinler",
                "C3a ve C5a moleküllerine verilen genel tıbbi isim"
            )
        ]
    })

    # Slide 58
    slides.append({
        "id": "k1-12-s58",
        "title": "Komplemanın Biyolojik Etkileri - II: C5a Aracılı Lökosit Kemotaksisi",
        "content": "C5a yalnızca bir anafilatoksin olmakla kalmaz; akut enflamasyonda **tüm lökositlerin (nötrofiller, monositler, eozinofiller ve bazofiller) en güçlü kemoatraktanlarından biridir**. Nötrofil yüzeyindeki C5aR1 (CD88) reseptörüne bağlandığında hücresel düzeyde şu kaskadı tetikler:\n\n1. **Kemotaktik Yönelim:** Nötrofillerde aktin polimerizasyonunu ve psödopod oluşumunu uyararak hücrelerin kemotaktik gradyent boyunca bakteriyel enfeksiyon odağına doğru süratle göç etmesini sağlar.\n2. **İntegrin Aktivasyonu:** Nötrofil yüzeyindeki beta-2 integrinlerin (CD11b/CD18 - Mac-1) konformasyonunu yüksek afiniteli açık forma dönüştürerek vasküler endoteldeki ICAM-1'e sıkıca kilitlenmelerini sağlar.\n3. **Oksidatif Patlama ve Degranülasyon:** Nötrofillerde NADPH oksidaz enzim kompleksini aktive ederek reaktif oksijen radikalleri (ROS) üretimini ve lizozomal enzimlerin salınımını tetikler; mikrobu yok etme hazırlığını tamamlar.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Lökosit Yanıtı", "C5a Aracılı Hücresel Mekanizma", "Enflamatuar Netice"],
                [
                    [
                        {"text": "Kemotaksi", "isMasked": False, "hint": ""},
                        {"text": "Aktin iskeletinin yeniden düzenlenmesi", "isMasked": True, "hint": "Yalancı ayak oluşturma hareketi"},
                        {"text": "Nötrofillerin enfeksiyon odağına hücumu", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Adezyon", "isMasked": False, "hint": ""},
                        {"text": "Beta-2 integrinlerin afinitesinin artması", "isMasked": True, "hint": "Endotele kenetlenme reseptörleri"},
                        {"text": "Damar duvarında durma ve transmigrasyon", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Aktivasyon", "isMasked": False, "hint": ""},
                        {"text": "NADPH oksidaz uyarımı ve enzim salınımı", "isMasked": True, "hint": "Mikrop öldürücü radikal patlaması"},
                        {"text": "Fagositoz ve mikrobisidal yıkım", "isMasked": False, "hint": ""}
                    ]
                ]
            ),
            make_recall(
                "Kompleman sisteminde nötrofiller için en güçlü kemotaktik ve aktive edici ajan olan parçacık hangisidir?",
                "C5a parçacığıdır.",
                "C5 parçalanmasıyla oluşan majör kemotaktik anafilatoksin"
            )
        ]
    })

    # Slide 59 (CHECKPOINT 6)
    slides.append({
        "id": "k1-12-s59",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 6] Kompleman Aktivasyon Yolları ve Efektör Moleküller",
        "content": "Kompleman sisteminin aktivasyonu ve temel efektör moleküllerinin sentezi:\n\n1. **Üç Yol:** Klasik yol antijen-antikorla (IgG, IgM); Alternatif yol doğrudan mikrop yüzeyi ve LPS ile; Lektin yolu MBL'nin bakteriyel mannoza bağlanmasıyla aktive olur.\n2. **C3 Konvertaz:** Klasik ve lektin yolunda C4b2a; alternatif yolda C3bBb'dir (Properdin ile stabilize edilir).\n3. **Merkezi Kesişme:** C3'ün C3a ve C3b'ye parçalanması tüm yolların ortak noktasıdır.\n4. **Anafilatoksinler (C3a, C5a):** Mast hücresinden histamin salarak vazodilatasyon ve venüler geçirgenlik artışı yaparlar.\n5. **Kemotaksi (C5a):** Nötrofil ve monositlerin en güçlü kemoatraktanıdır; integrin adezyonunu ve oksidatif patlamayı uyarır.\n6. **Opsonizasyon (C3b):** Mikrop yüzeyini kaplayarak fagositlerin CR1 reseptörüyle fagositozu dramatik artırır.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_quiz(
                "Kompleman sisteminin biyolojik fonksiyonları ve aracı molekülleriyle ilgili aşağıdaki eşleştirmelerden hangisi DOĞRUDUR?",
                [
                    {"key": "A", "text": "Opsonizasyon: C3b parçacığı aracılığıyla gerçekleştirilir.", "explanation": "A seçeneği DOĞRUDUR: C3b mikrop yüzeyine kovalent bağlanarak fagositik CR1 reseptörlerine hedef gösterir."},
                    {"key": "B", "text": "En güçlü kemoatraktan: C3a molekülüdür.", "explanation": "B seçeneği yanlıştır: En güçlü kemoatraktan C5a'dır."},
                    {"key": "C", "text": "Klasik C3 konvertaz: Yalnızca C3b ve Faktör B'den oluşur.", "explanation": "C seçeneği yanlıştır: C4b2a'dır."},
                    {"key": "D", "text": "Alternatif yol: IgG antikorları tarafından başlatılır.", "explanation": "D seçeneği yanlıştır: Antikordan bağımsızdır, mikrop yüzeyiyle başlar."},
                    {"key": "E", "text": "Anafilatoksinler: Trombositlerin pıhtılaşmasını tamamen durdurur.", "explanation": "E seçeneği yanlıştır: Mast hücresinden histamin salarlar."}
                ],
                "A"
            ),
            make_cloze(
                "Mikropların yüzeyine kovalent bağlanarak fagositozu kolaylastıran temel kompleman opsonini C3b molekülüdür.",
                "C3b molekülüdür",
                "Temel kompleman opsonizasyon proteini parçası"
            )
        ]
    })

    # Slide 60
    slides.append({
        "id": "k1-12-s60",
        "title": "Komplemanın Biyolojik Etkileri - III: C3b Opsonizasyonu ve Fagositoz",
        "content": "Kompleman sisteminin mikrobiyal enfeksiyonları temizlemedeki en kritik savunma mekanizması **opsonizasyondur** (Yunanca opsonein = yemeye hazır hale getirmek). Bakterilerin dış kapsülü (örneğin *Streptococcus pneumoniae*, *Haemophilus influenzae*) normalde nötrofil ve makrofajların fagositozundan kaçmalarını sağlar. Ancak kompleman aktive olduğunda binlerce **C3b ve iC3b** molekülü bakterinin hücre duvarına kovalent tiyoester bağlarıyla kenetlenir ve yüzeyi adeta bir 'sos gibi kaplar':\n\n- **Fagosit Reseptörleri (CR1 / CD35):** Nötrofil ve makrofaj membranlarında yüksek afiniteli Kompleman Reseptörü-1 (CR1) bulunur. CR1 mikrop üzerindeki C3b'ye kilitlenir.\n- **Fagositozun Tetiklenmesi:** Bu kenetlenme fagositozu yüzlerce kat hızlandırır; aktin polimerizasyonu ile mikrop fagozom içine yutulur ve lizozomlarla birleşerek dakikalar içinde imha edilir. C3 eksikliği olan hastalarda kapsüllü bakterilere bağlı tekrarlayan ölümcül piyojenik enfeksiyonlar görülmesinin sebebi opsonizasyonun çökmesidir.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "C3b Aracılı Opsonizasyon ve Yutulma Kaskadı",
                [
                    "1. Yüzey Kaplama: Binlerce aktif C3b molekülünün bakteri kapsülüne kovalent yapışması",
                    "2. CR1 Tanıma: Fagosit membranındaki Kompleman Reseptörü-1 ile C3b'nin kilitlenmesi",
                    "3. Psödopod Sarması: Fagositer hücre zarının mikrobu çepeçevre sararak fagozom oluşturması",
                    "4. Fagolizozomal Lizis: Lizozom enzimleriyle bakterinin hücre içi sindirimi"
                ]
            ),
            make_recall(
                "Nötrofil ve makrofajların yüzeyinde bulunarak mikrop üzerine yapışmış C3b moleküllerini tanıyan ve fagositozu başlatan reseptör hangisidir?",
                "Kompleman Reseptörü-1'dir (CR1 / CD35).",
                "C3b'ye bağlanan primer fagosit reseptörü"
            )
        ]
    })

    return slides
