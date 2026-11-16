# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_6_slides():
    slides = []

    # Slide 51
    slides.append({
        "id": "k1-17-s51",
        "title": "Neisseria gonorrhoeae Biyolojisi ve Virülans Faktörleri",
        "content": "Neisseria gonorrhoeae, insan mukozalarına son derece iyi adapte olmuş gram negatif bir diplokoktur:\n\n- **Morfoloji:** Çiftler halinde, birbirine bakan yüzeyleri düzleşmiş (kahve çekirdeği veya böbrek biçimli), hareketsiz ve sporsuzdur; oksidaz ve katalaz pozitiftir.\n- **Kilit Virülans Faktörleri (Sınav Spotu):**\n  1. **Piluslar (Fimbria):** Epitel hücrelerine ilk tutunmayı sağlar; antijenik varyasyonla sürekli aminoasit sırasını değiştirerek bağışıklıktan kaçar.\n  2. **Opa (Opasite) Proteinleri:** Mukozal hücrelere sıkı bağlanmayı ve hücre içine invazyonu (transsitoz) yönetir.\n  3. **Lipooligosakkarit (LOS):** Klasik gram negatif LPS'den farklı olarak O-antijen zincirinden yoksundur; aşırı derecede endotoksiktir ve yoğun nötrofil akınına (cerahat) yol açar.\n  4. **IgA1 Proteaz:** Mukozal salgılardaki Sekretuvar IgA antikorlarını menteşe bölgesinden parçalayarak lokal immün savunmayı felç eder.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_slider(
                "Pilus ve Opa Proteinleri vs IgA1 Proteaz Görevi",
                "Pilus ve Opa Proteinleri",
                "Mukozal epitele ilk ve sıkı yapışmayı sağlar; antijenik değişkenlikle antikorlardan kaçar.",
                "IgA1 Proteaz",
                "Mukozada bulunan koruyucu salgısal IgA antikorlarını enzimatik olarak parçalar ve invazyonu kolaylaştırır."
            ),
            make_cloze(
                "Neisseria gonorrhoeae'nin mukozal yüzeylerdeki sekretuvar antikorları parçalamak için salgıladığı virülans enzimine IgA1 proteaz denir.",
                "IgA1 proteaz",
                "Mukozal antikorları kesen bakteriyel enzim"
            )
        ]
    })

    # Slide 52
    slides.append({
        "id": "k1-17-s52",
        "title": "Gonokokta Direnç Tarihi: Birbiri Ardına Çöken Tedaviler",
        "content": "Neisseria gonorrhoeae, antibiyotik geliştirme tarihinin en hızlı direnç geliştiren 'süper bakterilerinden' biridir:\n\n- **1940'lar - Sülfonamidler:** Kullanıma girdikten birkaç yıl sonra tamamen etkisiz hale geldi.\n- **1970'ler - Penisilinler:** Başlangıçta çok düşük doz penisilinle kür sağlanırken; plazmid aracılı penisilinaz (beta-laktamaz) üreten suşların (PPNG) yayılmasıyla penisilin tedaviden tamamen çıktı.\n- **1980'ler - Tetrasiklinler:** Ribozomal koruma genleri (tetM) nedeniyle tetrasiklin etkinliğini yitirdi.\n- **2000'ler - Florokinolonlar (Siprofloksasin/Ofloksasin):** DNA giraz ve topoizomeraz IV genlerindeki tek nokta mutasyonlarıyla kinolon direnci fırladı ve tüm dünyada kılavuzlardan çıkarıldı.\n- **Günümüz Gerçeği:** Tek güvenilir oral veya parenteral sınıf olarak **üçüncü kuşak genişlemiş spektrumlu sefalosporinler (Seftriakson)** kalmıştır; sefalosporin direncini engellemek için **ikili kombine tedavi** zorunlu hale getirilmiştir.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_chain(
                "Gonokokta Tarihsel Antibiyotik Direnç Kronolojisi",
                [
                    "1. Sülfonamid İflası: 1940'larda mutasyonlarla direnç hızla yerleşti.",
                    "2. Penisilin Çöküşü: 1976'da plazmid kökenli penisilinaz salgılayan suşlar yayıldı.",
                    "3. Kinolon Direnci: 2000'lerde GyrA mutasyonlarıyla siprofloksasin tedaviden düştü.",
                    "4. Son Kale Seftriakson: Direnç gelişimini geciktirmek için ikili tedavi protokolü benimsendi."
                ]
            ),
            make_quiz(
                "Aşağıdaki antibiyotik sınıflarından hangisi Neisseria gonorrhoeae'de gelişen yaygın kromozomal mutasyonlar nedeniyle günümüzde gonore tedavisinde KESİNLİKLE önerilmemektedir?",
                [
                    {"key": "A", "text": "Üçüncü kuşak sefalosporinler (Seftriakson)", "isCorrect": False, "explanation": "Seftriakson günümüzün altın standardıdır."},
                    {"key": "B", "text": "Florokinolonlar (Siprofloksasin / Ofloksasin)", "isCorrect": True, "explanation": "Doğru cevap B'dir: Florokinolonlara karşı dünya çapında %70'in üzerinde direnç geliştiği için gonorede kullanımları terk edilmiştir."},
                    {"key": "C", "text": "Genişletilmiş spektrumlu makrolidler (Azitromisin)", "isCorrect": False, "explanation": "Azitromisin kombine tedavinin parçasıdır."},
                    {"key": "D", "text": "Aminoglikozidler (Gentamisin)", "isCorrect": False, "explanation": "Gentamisin alternatif kurtarma ajanıdır."}
                ]
            )
        ]
    })

    # Slide 53
    slides.append({
        "id": "k1-17-s53",
        "title": "Gonokok Direnç Mekanizmaları: Enzimler, PBP ve Eflüks Pompaları",
        "content": "Gonokokun antibiyotiklere karşı geliştirdiği moleküler kalkanlar son derece sofistike bir kombinasyondur (Sınav Spotu):\n\n- **1. Beta-Laktamaz (Penisilinaz - TEM-1 Plazmidi):**\n  - Plazmid aracılığıyla aktarılır; penisilin ve dar spektrumlu sefalosporinlerin beta-laktam halkasını hidroliz ederek parçalar.\n- **2. Penisilin Bağlayan Protein (PBP) Mutasyonları:**\n  - **penA geni mutasyonları:** PBP-2 hedef proteininin yapısı değişir; üçüncü kuşak sefalosporinler (seftriakson, sefiksim) hedefe bağlanamaz ve MİK (minimum inhibitör konsantrasyon) değerleri yükselir.\n- **3. Dışa Atım (Eflüks) Pompaları (MtrCDE Sistemi):**\n  - Bakteri hücresine giren antibiyotikleri (makrolidler, penisilinler, tetrasiklinler) aktif enerji harcayarak dışarı pompalar.\n- **4. Porin Mutasyonları (porB):** Dış membran porin kanallarını daraltarak antibiyotiklerin periplazmik aralığa geçişini engeller.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_table(
                ["Direnç Mekanizması", "Sorumlu Gen / Yapı", "Etkilenen Antibiyotik Sınıfı"],
                [
                    ["Beta-laktamaz Enzimi", "blaTEM-1 plazmidi", "Doğal ve amino-penisilinler"],
                    ["Değişmiş PBP-2 Hedefi", "penA mozaik mutasyonu", "Genişlemiş spektrumlu sefalosporinler (Seftriakson)"],
                    ["Eflüks Pompası Artışı", "mtrR represör mutasyonu (MtrCDE)", "Makrolidler, tetrasiklinler, beta-laktamlar"],
                    ["DNA Giraz Mutasyonu", "gyrA ve parC mutasyonları", "Florokinolonlar (Siprofloksasin)"]
                ]
            ),
            make_cloze(
                "Gonokok suşlarında penisilin ve sefalosporinlerin bağlandığı hedef protein olan PBP-2 yapısını değiştirerek direnç oluşturan gen penA genidir.",
                "penA",
                "PBP-2 mozaik mutasyon geninin adı"
            )
        ]
    })

    # Slide 54
    slides.append({
        "id": "k1-17-s54",
        "title": "Standart Kombine Tedavi Protokolü: Seftriakson + Azitromisin",
        "content": "Komplike olmamış ürogenital, anorektal ve faringeal gonore tedavisinde güncel standart kılavuz protokolü (Sınav Spotu):\n\n- **Standart Rejim (Çift Antibiyotik Kombinasyonu):**\n  - **Seftriakson 250 mg İM TEK DOZ** (Yeni kılavuzlarda kilolu hastalarda 500 mg önerilmektedir)\n  - **ARTI**\n  - **Azitromisin 1 g oral TEK DOZ**\n- **Neden İki Ayrı Antibiyotik Aynı Anda Verilir? (İki Kritik Gerekçe):**\n  1. **Seftriakson Direncini Önlemek:** Gonokokun son kale olan sefalosporinlere karşı direnç geliştirmesini sinerjistik ikinci bir etki mekanizmasıyla engellemek.\n  2. **Klamidya Ko-Enfeksiyonunu Tedavi Etmek:** Gonoreli hastaların %20-40'ında aynı anda semptomsuz Chlamydia trachomatis enfeksiyonu mevcuttur; tek doz Azitromisin klamidyayı da aynı seansta kür eder.\n- **Uygulama Kolaylığı:** Her iki ilaç da doğrudan klinikte hekim gözetiminde tek seansta uygulanabilir.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_slider(
                "Tek Başına Seftriakson vs Seftriakson + Azitromisin Kombinasyonu",
                "Tek Başına Seftriakson",
                "Gonoreyi temizleyebilir ancak klamidya ko-enfeksiyonunu atlar ve sefalosporin direncini hızlandırır.",
                "Seftriakson + Azitromisin Kombinasyonu",
                "Hem gonore hem klamidyayı tek seansta kür eder; çapraz direnç gelişimini güçlü biçimde frenler."
            ),
            make_quiz(
                "Komplike olmamış gonokokal üretrit tanısı alan bir hastada kılavuzların önerdiği standart birinci basamak ikili tedavi rejimi hangisidir?",
                [
                    {"key": "A", "text": "Seftriakson 1x250 mg İM tek doz + Azitromisin 1 g oral tek doz", "isCorrect": True, "explanation": "Doğru cevap A'dır: Gonorede standart güncel kılavuz protokolü Seftriakson 250 mg İM + Azitromisin 1 g oral tek dozdur."},
                    {"key": "B", "text": "Siprofloksasin 500 mg oral tek doz", "isCorrect": False, "explanation": "Kinolon direnci nedeniyle kesinlikle önerilmez."},
                    {"key": "C", "text": "Metronidazol 2 g oral tek doz", "isCorrect": False, "explanation": "Metronidazol gonokoka etkisizdir."},
                    {"key": "D", "text": "Benzatin penisilin G 2.4 milyon ünite", "isCorrect": False, "explanation": "Bu sifiliz tedavisidir, gonorede penisilinaz nedeniyle etkisizdir."}
                ]
            )
        ]
    })

    # Slide 55
    slides.append({
        "id": "k1-17-s55",
        "title": "Azitromisin Alerjisinde Alternatif Rejim: Doksisiklin Seçeneği",
        "content": "Klinik pratikte hastanın makrolid (azitromisin) alerjisi veya intoleransı olması durumunda protokol modifiye edilir (Sınav Spotu):\n\n- **Klinik Senaryo:** Hasta gonore kliniği ile başvuruyor; ancak geçmişinde azitromisin veya klaritromisin kullanımına bağlı ürtiker, anjiyoödem veya şiddetli intolerans öyküsü veriyor.\n- **Kılavuz Rejimi:**\n  - **Seftriakson 250 mg İM tek doz**\n  - **ARTI**\n  - **Doksisiklin 2x100 mg oral, 7 gün**\n- **Rejimin Mantığı:**\n  - Seftriakson güçlü bakterisidal etkisiyle gonokok suşunu tek dozda öldürür.\n  - Doksisiklin ise azitromisinin yerine geçerek olası Chlamydia trachomatis ko-enfeksiyonunu 7 gün içinde tamamen temizler.\n- **Önemli Kısıtlama:** Bu rejim gebe kadınlarda doksisiklin kontrendikasyonu nedeniyle KULLANILAMAZ; gebede eritromisin veya amoksisilin seçilmelidir.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_table(
                ["Hasta Durumu", "Birinci Tercih Rejim", "İkinci Tercih / Alternatif Rejim"],
                [
                    ["Standart Gonore Olgusu", "Seftriakson 250 mg İM + Azitromisin 1 g oral", "Yok"],
                    ["Azitromisin Alerjisi Olan Hasta", "Seftriakson 250 mg İM + Doksisiklin 2x100 mg 7 gün", "Levofloksasin ile kombinasyon"]
                ]
            ),
            make_cloze(
                "Gonoreli bir hastada azitromisin alerjisi bulunması durumunda seftriaksonun yanına eklenen klamidya ilacı doksisiklin oral ajanıdır.",
                "doksisiklin",
                "Azitromisin alerjisinde 7 gün verilen tetrasiklin ajanı"
            )
        ]
    })

    # Slide 56
    slides.append({
        "id": "k1-17-s56",
        "title": "Sefalosporin Alerjisi ve Penisilin Anafilaksisinde Kurtarma Tedavisi",
        "content": "Gonore tedavisinin en zorlu klinik tablosu hastada sefalosporin veya ağır penisilin anafilaksi öyküsü bulunmasıdır (Sınav Spotu):\n\n- **Klinik Zorluk:** Penisiline bağlı anafilaksi veya sefalosporin alerjisi olan hastada Seftriakson kullanılamaz (çapraz reaksiyon ve fatal şok riski).\n- **CDC ve Sağlık Bakanlığı Onaylı Kurtarma Protokolleri:**\n  1. **Seçenek 1 (Kinolon + Yüksek Doz Makrolid):**\n     - **Gemifloksasin 1x320 mg oral TEK DOZ**\n     - **ARTI**\n     - **Azitromisin 2 g oral TEK DOZ** (yüksek doz azitromisin)\n  2. **Seçenek 2 (Aminoglikozid + Yüksek Doz Makrolid):**\n     - **Gentamisin 1x240 mg İM TEK DOZ**\n     - **ARTI**\n     - **Azitromisin 2 g oral TEK DOZ**\n- **Neden Azitromisin 2 Gram?** Sefalosporin verilemediği için gonokokun eradikasyonunu garantilemek ve olası dirençleri aşmak amacıyla azitromisin dozu 1 gramdan 2 grama katlanır.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_table(
                ["Alerji Durumu", "Kurtarma Kombinasyonu", "Dozaj ve Uygulama", "Tedavi Süresi"],
                [
                    ["Sefalosporin Alerjisi (Seçenek 1)", "Gemifloksasin + Azitromisin", "Gemifloksasin 320 mg oral + Azitromisin 2 g oral", "Tek doz"],
                    ["Sefalosporin Alerjisi (Seçenek 2)", "Gentamisin + Azitromisin", "Gentamisin 240 mg İM + Azitromisin 2 g oral", "Tek doz"]
                ]
            ),
            make_quiz(
                "Geçmişinde penisilin ve sefalosporinlere bağlı anafilaktik şok öyküsü bulunan gonoreli bir hastada kılavuzlara göre uygulanabilecek en uygun birinci kurtarma rejimi nedir?",
                [
                    {"key": "A", "text": "Gentamisin 240 mg İM tek doz + Azitromisin 2 g oral tek doz", "isCorrect": True, "explanation": "Doğru cevap A'dır: Sefalosporin ve beta-laktam alerjisinde Gentamisin (240 mg İM) + Azitromisin (2 g oral) veya Gemifloksasin + Azitromisin uygulanır."},
                    {"key": "B", "text": "Ampisilin/sulbaktam İV", "isCorrect": False, "explanation": "Penisilin anafilaksisinde kesinlikle kontrendikedir."},
                    {"key": "C", "text": "Sefazolin 1 g İM", "isCorrect": False, "explanation": "Sefalosporindir, alerjide kullanılamaz."},
                    {"key": "D", "text": "Sadece aspirin", "isCorrect": False, "explanation": "Antibiyotik değildir."}
                ]
            )
        ]
    })

    # Slide 57
    slides.append({
        "id": "k1-17-s57",
        "title": "Neisseria gonorrhoeae Kültürü: Thayer-Martin ve CO2 Şartı",
        "content": "Gonokok son derece nazlı (fastidious) bir mikroorganizmadır; laboratuvar ekiminde özel koşullar gerektirir (Sınav Spotu):\n\n- **1. Seçici Besiyeri (Modifiye Thayer-Martin Besiyeri):**\n  - Çikolatamsı agar temeline diğer kommensal mikropları baskılayan 4 majör antibiyotik eklenmiştir:\n    - **Vankomisin:** Gram pozitif bakterileri baskılar.\n    - **Kolistin:** Diğer gram negatif basilleri baskılar.\n    - **Nistatin:** Maya ve mantarları baskılar.\n    - **Trimetoprim:** Proteus'un yayılmasını (swarming) engeller.\n- **2. Atmosferik Koşullar:**\n  - Bakteri kapnofiliktir; **%5-10 CO2 içeren nemli ortamda**, 35-37°C'de inkübe edilmelidir.\n- **3. Hasta Başı Ekim (Bedside Inoculation):**\n  - Gonokok soğuğa ve kurumaya aşırı duyarlıdır; sürüntü pamuğu bekletilirse hızla ölür; eküvyon alınır alınmaz **hasta başında doğrudan besiyerine ekilmeli** veya özel taşıma besiyerine (Transgrow/JEMBEC) konmalıdır.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_slider(
                "Standart Besiyeri vs Modifiye Thayer-Martin Besiyeri",
                "Standart Kanlı Agar",
                "Tüm genital kommensal bakteriler hızla ürer ve gonokok kolonilerini tamamen bastırır.",
                "Thayer-Martin Besiyeri",
                "Vankomisin, kolistin, nistatin ve trimetoprim içerir; diğer tüm florayı baskılayıp sadece Neisseria'yı üretir."
            ),
            make_cloze(
                "Neisseria gonorrhoeae izolasyonu için vankomisin, kolistin, nistatin ve trimetoprim içeren özel seçici besiyerine Thayer-Martin besiyeri denir.",
                "Thayer-Martin",
                "Gonokok için kullanılan özel antibiyotikli seçici agar"
            )
        ]
    })

    # Slide 58
    slides.append({
        "id": "k1-17-s58",
        "title": "Faringeal ve Rektal Gonore: Lokal Penetrasyon Güçlüğü",
        "content": "Gonokok cinsel pratiklere bağlı olarak yalnızca ürogenital sistemi değil, farenks ve rektumu da tutar:\n\n- **Faringeal Gonore (Boğaz Gonoresi):**\n  - Oral seks yoluyla bulaşır; hastaların **%90'ından fazlası tamamen asemptomatiktir** (sessiz farenjit).\n  - Boğaz mukozasında antibiyotik penetrasyonu çok zayıftır; oral sefiksim bu bölgede başarısız olur.\n  - Bu nedenle faringeal gonorede mutlaka yüksek doku düzeyine ulaşan **Seftriakson 250 mg İM + Azitromisin 1 g oral** verilmelidir.\n- **Rektal Gonore (Gonokokal Proktit):**\n  - Reseptif anal seks sonrası gelişir; rektal akıntı, kaşıntı, tenesmus ve dışkılama sırasında kanama yapabilir.\n  - Tanıda rektal sürüntüde NAAT veya kültür kullanılır; tedavi yine standart Seftriakson + Azitromisin protokolüdür.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_table(
                ["Anatomik Bölge", "Bulaş Yolu", "Semptom Durumu", "Zorunlu İlaç"],
                [
                    ["Farenks (Boğaz)", "Oral seks", "%90 asemptomatik (sessiz rezervuar)", "Mutlaka Seftriakson İM (oral sefiksim yetersiz)"],
                    ["Rektum (Proktit)", "Anal seks", "Tenesmus, mukopürülan akıntı, kanama", "Standart Seftriakson + Azitromisin"]
                ]
            ),
            make_quiz(
                "Oral seks sonrası faringeal gonore saptanan asemptomatik bir hastada oral sefalosporinlerin (sefiksim) yetersiz kalmasının ve Seftriakson İM tercih edilmesinin temel nedeni nedir?",
                [
                    {"key": "A", "text": "Farenks mukozasında antibiyotik penetrasyonunun zayıf olması ve Seftriakson'un daha yüksek doku konsantrasyonu sağlaması", "isCorrect": True, "explanation": "Doğru cevap A'dır: Farenks gonokokunun temizlenmesi ürogenital bölgeye göre çok daha zordur; yüksek doku seviyesi sağlayan parenteral Seftriakson şarttır."},
                    {"key": "B", "text": "Boğazdaki bakterilerin fotosentez yapması", "isCorrect": False, "explanation": "Gonokok fotosentez yapmaz."},
                    {"key": "C", "text": "Farenksin sadece virüslerle enfekte olabilmesi", "isCorrect": False, "explanation": "Bakteriler de farenkste kolonize olur."},
                    {"key": "D", "text": "Hastanın tükürüğünün tüm antibiyotikleri yok etmesi", "isCorrect": False, "explanation": "Bilim dışı açıklama."}
                ]
            )
        ]
    })

    # Slide 59 - CHECKPOINT 6
    slides.append({
        "id": "k1-17-s59",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 6] Gonokok Enfeksiyonu ve Direnç Tedavisi",
        "content": "Bu checkpointte Neisseria gonorrhoeae virülansını, direnç mekanizmalarını ve güncel tedavi şemalarını özetliyoruz:\n\n- **Virülans:** Pilus (tutunma ve antijenik varyasyon), Opa proteinleri (invazyon), LOS (endotoksisite ve nötrofil akını), IgA1 proteaz (mukozal antikor yıkımı).\n- **Direnç Evrimi:** Penisilin, tetrasiklin ve florokinolonlar direnç nedeniyle tamamen devre dışı kalmıştır; tek güvenilir sınıf sefalosporinlerdir.\n- **Standart Rejim:** Seftriakson 250 mg İM tek doz + Azitromisin 1 g oral tek doz (klamidya ko-enfeksiyonunu da temizler).\n- **Azitromisin Alerjisi:** Seftriakson 250 mg İM + Doksisiklin 2x100 mg 7 gün.\n- **Sefalosporin / Penisilin Anafilaksisi:** Gemifloksasin 320 mg oral + Azitromisin 2 g oral VEYA Gentamisin 240 mg İM + Azitromisin 2 g oral.\n- **Laboratuvar:** Modifiye Thayer-Martin besiyeri (vankomisin, kolistin, nistatin, trimetoprim), %10 CO2, hasta başı ekim.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_table(
                ["Klinik Durum", "Birinci Tercih İlaç", "Uygulama Yolu ve Doz"],
                [
                    ["Standart Gonore Tedavisi", "Seftriakson + Azitromisin", "250 mg İM tek doz + 1 g oral tek doz"],
                    ["Azitromisin Alerjisi", "Seftriakson + Doksisiklin", "250 mg İM tek doz + 2x100 mg oral 7 gün"],
                    ["Sefalosporin Anafilaksisi (Oral)", "Gemifloksasin + Azitromisin", "320 mg oral tek doz + 2 g oral tek doz"],
                    ["Sefalosporin Anafilaksisi (Parenteral)", "Gentamisin + Azitromisin", "240 mg İM tek doz + 2 g oral tek doz"]
                ]
            ),
            make_chain(
                "Gonore Tedavi Seçim Algoritması",
                [
                    "1. Gonore Tanısı: Gram yaymada diplokok veya NAAT pozitifliği.",
                    "2. Alerji Sorgulaması: Sefalosporin ve makrolid alerjisi sorgulanır.",
                    "3. Standart Protokol: Alerji yoksa Seftriakson 250 mg İM + Azitromisin 1 g verilir.",
                    "4. Ağır Alerji Durumu: Gentamisin 240 mg İM + Azitromisin 2 g oral kurtarma uygulanır."
                ]
            )
        ]
    })

    # Slide 60
    slides.append({
        "id": "k1-17-s60",
        "title": "Bölüm Özeti: Gonokoktan Pelvik İnflamatuvar Hastalık (PİH) Tedavisine Geçiş",
        "content": "Bölüm 6 boyunca Neisseria gonorrhoeae virülans faktörlerini, direnç evrimini ve ikili antibiyotik yönetimini tamamladık:\n\n- **Kritik İlke:** Gonore tedavisinde tek ilaç kullanımı direnci tetikler; Seftriakson daima Azitromisin (veya Doksisiklin) ile kombine edilmelidir.\n- **Sonraki Bölüm:** Bir sonraki bölümde klamidya ve gonorenin en tehlikeli üst genital komplikasyonu olan **Pelvik İnflamatuvar Hastalığı (PİH), hastaneye yatış endikasyonlarını ve parenteral İV tedavi protokollerini** inceleyeceğiz.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_recall(
                "Neisseria gonorrhoeae izolasyonunda kullanılan ve vankomisin, kolistin, nistatin ile trimetoprim içeren seçici çikolatamsı besiyeri nedir?",
                "Modifiye Thayer-Martin besiyeri",
                "Gonokok için kullanılan 4 antibiyotikli özel besiyeri"
            ),
            make_quiz(
                "Aşağıdakilerden hangisi gonore tedavisinde Seftriakson'un yanına mutlaka Azitromisin eklenmesinin iki temel gerekçesinden biridir?",
                [
                    {"key": "A", "text": "Hastanın iştahını açarak kilo almasını sağlamak", "isCorrect": False, "explanation": "İştah açıcı etkisi yoktur."},
                    {"key": "B", "text": "Gonokokta sefalosporin direncini engellemek ve eşlik eden Chlamydia trachomatis ko-enfeksiyonunu aynı anda tedavi etmek", "isCorrect": True, "explanation": "Doğru cevap B'dir: Kombinasyon sefalosporin direncini frenler ve %20-40 oranında eşlik eden klamidyayı temizler."},
                    {"key": "C", "text": "Hastada kan basıncını yükseltmek", "isCorrect": False, "explanation": "Kan basıncıyla ilişkisizdir."},
                    {"key": "D", "text": "Eritrosit üretimini iki katına çıkarmak", "isCorrect": False, "explanation": "Eritropoietik etkisi yoktur."}
                ]
            )
        ]
    })

    return slides
