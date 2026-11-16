# -*- coding: utf-8 -*-
from .helpers import make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall

def get_section_2_slides():
    slides = []

    # Slide 11
    slides.append({
        "id": "k1-11-s11",
        "title": "Böbrek Düzeyindeki Obstrüksiyon Nedenleri: Konjenital ve Neoplastik",
        "content": "Böbrek düzeyindeki obstrüksiyonlar toplayıcı sistemin en üst noktasını, kaliksleri ve renal pelvisi ilgilendirir:\n\n- **Konjenital Lezyonlar:**\n  - **Üreteropelvik Bileşke (UPJ) Darlığı:** En sık konjenital supravezikal nedendir; üreter düz kas liflerinin adizorganize olması veya fibröz striktür sonucu pelvis ile üreter geçişi bozulur.\n  - **Aberran / Aksesuar Renal Damar:** Alt pol renal arteri renal pelvis ve üreteri önden çaprazlayarak mekanik extrinsic kompresyon yapar.\n  - **Polikistik Böbrek ve Peripelvik Kistler:** Parankim ve sinüsteki büyük kistler toplayıcı infundibulumları bası altında bırakır.\n- **Neoplastik Lezyonlar:**\n  - **Renal Hücreli Karsinom (RCC):** Kitle etkisiyle kaliks basısı.\n  - **Renal Pelvis Transizyonel Hücreli Karsinomu (TCC/Ürotelyal Karsinom):** İntralüminal obstrüktif polipoid kitle oluşturur.\n  - **Wilms Tümörü (Nefroblastom):** Çocukluk çağında parankimal aşırı büyüme ile toplayıcı sistem basısı.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_cloze(
                "Renal pelvis çıkımında aberran alt pol damarı ekstrinsik bası yaparak üreteropelvik bileske darlığı tablosuna yol açabilir.",
                "üreteropelvik bileske darlığı",
                "Pelvis ile üreter arasındaki kritik geçiş bölgesi patolojisi"
            ),
            make_quiz(
                "Böbrek düzeyinde intralüminal polipoid kitle yaparak obstrüksiyona ve hematüriye neden olan toplayıcı sistem epitelyal malignitesi hangisidir?",
                [
                    {"key": "A", "text": "Renal anjiyomiyolipom", "explanation": "A seçeneği yanlıştır: Benign mezenkimal lezyondur."},
                    {"key": "B", "text": "Renal pelvis ürotelyal karsinomu (TCC)", "explanation": "B seçeneği doğrudur: Pelvis toplayıcı epitelinden köken alarak lümen içi obstrüksiyon ve makroskopik hematüri yapar."},
                    {"key": "C", "text": "Basit kortikal kist", "explanation": "C seçeneği yanlıştır: Dışa doğru büyür, lümen içi kitle yapmaz."},
                    {"key": "D", "text": "Prostat adenokarsinomu", "explanation": "D seçeneği yanlıştır: İnfravezikal seviye tümörüdür."},
                    {"key": "E", "text": "Echinococcus kist hidatiği", "explanation": "E seçeneği yanlıştır: Paraziter enfeksiyondur, epitelyal malignite değildir."}
                ],
                "B"
            )
        ]
    })

    # Slide 12
    slides.append({
        "id": "k1-11-s12",
        "title": "Böbrek Düzeyindeki Obstrüksiyon Nedenleri: İnflamatuar ve Metabolik",
        "content": "Böbrek parankimi ve kaliksiyel yapıyı etkileyen non-neoplastik durumlar lümeni daraltabilir:\n\n- **İnflamatuar ve Enfeksiyöz Nedenler:**\n  - **Renal Tüberküloz:** Papiller kavitasyon, granülomatöz skar ve infundibulum striktürlerine ('kadeh kadeh toplayıcı sistem kopuklukları') yol açar.\n  - **Echinococcus Granulosus (Kist Hidatik):** Kistin toplayıcı sisteme açılması sonucu yavru veziküllerin ve membranların kaliksleri tıkaması.\n- **Metabolik ve Diğer Faktörler:**\n  - **Nefrolitiyazis:** Renal pelvisi dolduran geyik boynuzu (staghorn) taşlar veya kaliks taşları.\n  - **Renal Papiller Nekroz:** Diyabetik veya analjezik nefropatili hastalarda nekroze olan papilla parçasının kaliks boynuna düşerek akut mekanik blokaj yapması.\n  - **Multipl Miyelom:** Bence Jones protein silendirlerinin tübülleri tıkayarak tübüler düzeyde obstrüksiyon oluşturması.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_chain(
                "Papiller Nekrozda Akut Obstrüksiyon Akışı",
                [
                    "1. Medüller İskemi: Diyabet veya NSAİİ kullanımı ile medüller mikrodolaşımın çökmesi",
                    "2. Papilla Uç Nekrozu: Renal piramid ucunun iskemik nekrozla toplayıcı sisteme kopması",
                    "3. Kaliks Ağzına Düşme: Nekrotik doku parçasının infundibulum veya UPJ lümenine oturması",
                    "4. Akut Üreter Tıkanması: Papilla dokusunun üreteri mekanik olarak tıkaması",
                    "5. Akut Renal Kolik ve Hematüri: Doku parçasının atılamaması sonucu şiddetli böğür ağrısı"
                ]
            ),
            make_recall(
                "Diyabetik bir hastada akut böğür ağrısı ve dökülen doku parçaları ile giden obstrüktif üropati nedeni nedir?",
                "Renal papiller nekrozdur; sloughing olan papilla lümeni tıkar.",
                "Medüller papilla doku dökülmesi"
            )
        ]
    })

    # Slide 13
    slides.append({
        "id": "k1-11-s13",
        "title": "Üreter Düzeyindeki Obstrüksiyon Nedenleri: İntrensek Patolojiler",
        "content": "Üreter yaklaşık 25-30 cm uzunluğunda dar bir lümene sahip olduğundan intrensek lezyonlara karşı oldukça duyarlıdır:\n\n1. **Ürolitiyazis (Üreter Taşları):** En yaygın akut üreter obstrüksiyonu nedenidir. Taş en sık üç anatomik darlıkta takılır:\n   - Üreteropelvik bileşke (UPJ)\n   - İliak damarları çaprazladığı pelvik kenar\n   - Üreterovezikal bileşke (UVJ - intramural üreter; en dar yerdir)\n2. **Konjenital Anomaliler:** Üreteral valv, üreterosel (intramural üreterin kistik balonlaşması), çift toplayıcı sistem ektopik üreter açılımı.\n3. **Üreter Tümörleri:** Primer üreter ürotelyal karsinomu lümende 'kadeh belirtisi' oluşturarak akımı durdurur.\n4. **Kan Pıhtısı ve Sloughing Doku:** Üst sistem kanamalarında pıhtının üreterde organize olması.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_table(
                ["Anatomik Darlık Bölgesi", "Lokalizasyon Özelliği", "Klinik Taş Takılma Sıklığı"],
                [
                    [
                        {"text": "Üreterovezikal Bileşke (UVJ)", "isMasked": False, "hint": ""},
                        {"text": "İntramural mesane duvarı geçişi (en dar nokta)", "isMasked": True, "hint": "Üreterin mesane kas tabakası içindeki en dar tüneli"},
                        {"text": "En sık taş takılma bölgesi", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "İliak Damar Çaprazı", "isMasked": False, "hint": ""},
                        {"text": "Pelvis giriminde damarların oluşturduğu açı", "isMasked": True, "hint": "Büyük damarların üreteri alttan desteklediği büklüm"},
                        {"text": "İkinci sıklıkta takılma yeri", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Üreteropelvik Bileşke (UPJ)", "isMasked": False, "hint": ""},
                        {"text": "Pelvis hunisinden üreter tüpüne geçiş", "isMasked": True, "hint": "Geniş hazneden dar tüpe ilk giriş bölgesi"},
                        {"text": "Giriş darlığı bölgesi", "isMasked": False, "hint": ""}
                    ]
                ]
            ),
            make_recall(
                "Üreterin tüm trasesi boyunca lümenin en dar olduğu ve üreter taşlarının en sık impakte olduğu anatomik darlık neresidir?",
                "Üreterovezikal bileşke (UVJ) / intramural üreterdir.",
                "Mesane duvarına giriş bölgesi"
            )
        ]
    })

    # Slide 14
    slides.append({
        "id": "k1-11-s14",
        "title": "Üreter Düzeyindeki Obstrüksiyon Nedenleri: Ekstrinsik Patolojiler",
        "content": "Üreter retroperitoneal yerleşimi nedeniyle çevre dokuların patolojilerinden sıkça etkilenir:\n\n- **Retroperitoneal Fibrozis (Ormond Hastalığı):** Üreterleri mediyale doğru çeken ve dıştan saran yoğun idiyopatik fibrotik plak.\n- **Pelvik Maligniteler:** İlerlemiş serviks kanseri, rektum kanseri, prostat kanseri ve retroperitoneal lenf nodu metastazları.\n- **Vasküler Anomaliler ve Anevrizmalar:**\n  - **Retrokaval Üreter (Sirkumkaval):** Sağ üreterin vena cava inferiorun arkasından dolanması sonucu basıya uğraması.\n  - Abdominal aort veya iliak arter anevrizmaları.\n- **Jinekolojik ve Obstetrik Durumlar:**\n  - **Gebelik Hidronefrozu:** Büyüyen uterusun mekanik basısı ve yüksek progesteron hormonunun düz kas gevşetici etkisi (özellikle sağ tarafta belirgindir).\n  - **Endometriozis:** Üreter serozasında yerleşen endometriyal odakların siklik kanama ve fibrozis yapması.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_cloze(
                "Gebelikte üreter dilatasyonunun sag tarafta daha belirgin olmasının nedeni deksorotasyon ve sağ ovaryan ven pleksusunun basısıdır.",
                "sag tarafta",
                "Gebelik hidronefrozunun anatomik olarak asimetrik yoğunlaştığı taraf"
            ),
            make_quiz(
                "Retroperitoneal fibrozis (Ormond hastalığı) tablosunda üreterlerin karakteristik radyolojik görünümü nasıldır?",
                [
                    {"key": "A", "text": "Üreterler aşırı derecede laterale deplase olur ve kıvrımlaşır.", "explanation": "A seçeneği yanlıştır: Fibrozis üreterleri laterale değil mediyale çeker."},
                    {"key": "B", "text": "Üreterler orta hatta doğru (mediyale) çekilir ve dıştan saran fibröz doku nedeniyle daralır.", "explanation": "B seçeneği doğrudur: Ormond hastalığında üreterlerin mediyale deviyasyonu tipiktir."},
                    {"key": "C", "text": "Üreterlerde yaygın divertiküller ve sakküller oluşur.", "explanation": "C seçeneği yanlıştır: Bu durum mesane çıkış obstrüksiyonlarında mesanede görülür."},
                    {"key": "D", "text": "Üreter lümeninde çok sayıda kist hidatik yavru vezikülü izlenir.", "explanation": "D seçeneği yanlıştır: Paraziter enfeksiyon bulgusudur."},
                    {"key": "E", "text": "Üreter tamamen kalsifiye olup 'porselen üreter' görünümü alır.", "explanation": "E seçeneği yanlıştır: Şistozomiyazis veya tüberkülozda görülebilen tablodur."}
                ],
                "B"
            )
        ]
    })

    # Slide 15
    slides.append({
        "id": "k1-11-s15",
        "title": "Gebelikte Üriner Obstrüksiyon ve Hidroüreteronefroz",
        "content": "Gebelikte fizyolojik olarak toplayıcı sistemde dilatasyon izlenir ve bu tablo bazen obstrüktif semptomlar verebilir:\n\n- **Mekanik Neden:** Büyüyen gravür uterusun pelvik brim düzeyinde üreterleri sıkıştırması.\n- **Hormonal Neden:** Yüksek **progesteron** seviyeleri üreter düz kas tonusunu ve peristaltik dalga amplitüdünü belirgin derecede azaltır.\n- **Sağ Taraf Baskınlığı:** Gebe kadınların %80-90'ında dilatasyon sağ üreterde çok daha belirgindir. Bunun sebepleri:\n  1. Uterusun fizyolojik sağa rotasyonu (dekstrorotasyon).\n  2. Sağ ovaryan ven pleksusunun sağ üreteri çaprazlarken oluşturduğu bası.\n  3. Sol üreterin sigmoid kolon tarafından bir miktar korunması.\n\n> [!TIP]\n> Gebelik hidronefrozu doğumdan sonra 6-12 hafta içinde kendiliğinden normale döner; enfeksiyon eklenmedikçe agresif invaziv girişimlerden kaçınılır.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_slider(
                "Normal Non-Gebe Üreter",
                "Düzenli peristaltik ritim (dakikada 2-6 dalga), normal lümen kalibresi, düşük intralüminal basınç.",
                "Gebelikteki Üreter (Özellikle Sağ)",
                "Progesterona bağlı hipotonisite, peristaltizmde yavaşlama, uterus basısıyla belirgin pelvik ve kaliksiyel dilatasyon."
            ),
            make_recall(
                "Gebelikte üreter düz kaslarında relaksasyona ve toplayıcı sistem dilatasyonuna yol açan primer hormon hangisidir?",
                "Progesterondur.",
                "Gebeliği koruyan majör korpus luteum ve plasenta hormonu"
            )
        ]
    })

    # Slide 16
    slides.append({
        "id": "k1-11-s16",
        "title": "Mesane ve Prostat Düzeyindeki Obstrüksiyon Nedenleri",
        "content": "Mesane çıkımı ve prostatik patolojiler erişkin çağın en yaygın kronik obstrüksiyon kaynağıdır:\n\n- **Benign Prostat Hiperplazisi (BPH):** İleri yaş erkeklerde prostatın transizyonel zonundaki stromal ve glandüler hiperplazi hem mekanik bası hem de artmış alfa-adrenerjik tonusla idrar akımını engeller.\n- **Prostat Adenokarsinomu:** Periferik zon kaynaklı olsa da lokal ileri evrede üretra ve mesane boynunu infiltre eder.\n- **Nöropatik (Nörojenik) Mesane:**\n  - Spina bifida, meningomiyelosel, diyabetik nöropati, spinal kord travmaları veya multipl skleroz.\n  - Detrüsör-sfinkter dissinerjisi: Mesane kasılırken eksternal sfinkterin gevşeyememesi çok yüksek basınçlı fonksiyonel obstrüksiyon üretir.\n- **Mesane Tümörleri:** Mesane boynuna veya üreter orifislerine oturan kas invaziv karsinomlar.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_branching(
                "68 yaşında erkek hasta, geceleri 5 kez idrara kalkma, idrar başlatırken bekleme ve kesik kesik işeme yakınmaları ile başvuruyor. Rektal muayenede prostat 60 gram, elastik ve ağrısız palpe ediliyor.",
                "Bu hastadaki obstrüksiyonun tipi ve primer mekanizması hangisidir?",
                [
                    {
                        "text": "Kronik infravezikal obstrüksiyon (BPH'ya bağlı mekanik ve dinamik çıkım direnci)",
                        "outcome": "Doğru klinik yaklaşım: BPH transizyonel zon hiperplazisiyle mesane çıkımını daraltarak klasik infravezikal obstrüksiyon semptomları oluşturur.",
                        "isOptimal": True
                    },
                    {
                        "text": "Akut supravezikal tek taraflı üreter obstrüksiyonu",
                        "outcome": "Hatalı: Supravezikal tek taraflı lezyonlar işeme güçlüğü veya BPH semptomu yapmaz.",
                        "isOptimal": False
                    },
                    {
                        "text": "Akut bakteriyel sistit atağı",
                        "outcome": "Hatalı: Yavaş ilerleyen noktüri ve hesitans semptomları kronik obstrüksiyon bulgusudur.",
                        "isOptimal": False
                    }
                ]
            )
        ]
    })

    # Slide 17
    slides.append({
        "id": "k1-11-s17",
        "title": "Üretra Düzeyindeki Obstrüksiyon Nedenleri",
        "content": "Üretra lezyonları akımın en distal engelidir:\n\n- **Konjenital Lezyonlar:**\n  - **Posterior Üretral Valv (PUV):** Yalnızca erkek çocuklarda görülen, prostatik üretrada anormal mukoza kıvrımının tek yönlü valv gibi akımı tıkaması.\n  - **Konjenital Mea Darlığı / Fimozis:** Sünnet derisi veya eksternal meatustaki darlık.\n- **Edinsel Lezyonlar:**\n  - **Üretra Darlığı (Striktür):** İatrojenik (kateterizasyon, endoskopik cerrahi), travmatik (straddle/ata biner tarzda düşme) veya gonokoksik üretrit skarı.\n  - **Üretra Taşları:** Mesaneden düşen taşın penil üretraya oturması.\n  - **Pelvik Kırık ve Üretra Distraksiyon Hasarı:** Membranöz üretranın komplet kopması.\n  - **Periüretral Apse:** Üretra bezlerinin enfeksiyonu ile lümene bası.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_cloze(
                "Pelvik travma veya iatrojenik kateterizasyona bagli uretra yaralanmalari iyilesirken fibröz skar dokusu olusturarak uretra darligi gelisimine neden olur.",
                "uretra darligi",
                "İdrar kanalında lümenin fibröz dokuyla büzüşmesi durumu"
            ),
            make_quiz(
                "Genç bir erkekte bisiklet kadrosuna düşme (ata biner tarzda travma) sonrası gelişebilecek en tipik üriner obstrüksiyon etiyolojisi nedir?",
                [
                    {"key": "A", "text": "Renal arter anevrizması", "explanation": "A seçeneği yanlıştır: Damarsal renal patolojidir."},
                    {"key": "B", "text": "Bulber üretra kontüzyonu ve post-travmatik üretra darlığı", "explanation": "B seçeneği doğrudur: Perineal straddle yaralanmalarında bulber üretra simfizis pubise sıkışarak travmatik darlık oluşturur."},
                    {"key": "C", "text": "Benign prostat hiperplazisi", "explanation": "C seçeneği yanlıştır: Yaşlılık hastalığıdır."},
                    {"key": "D", "text": "Üreterovezikal darlık", "explanation": "D seçeneği yanlıştır: Üst üriner sistem konjenital darlığıdır."},
                    {"key": "E", "text": "Retroperitoneal fibrozis", "explanation": "E seçeneği yanlıştır: Sistemik immün kaynaklı plak hastalığıdır."}
                ],
                "B"
            )
        ]
    })

    # Slide 18
    slides.append({
        "id": "k1-11-s18",
        "title": "İlaçlara Bağlı Fonksiyonel Üriner Obstrüksiyon",
        "content": "Bazı sistemik ilaçlar mesane ve sfinkter fonksiyonlarını doğrudan bozarak obstrüksiyona ve retansiyona yol açar:\n\n1. **Antikolinerjik İlaçlar:** Atropin, skopolamin, oksibutinin, trisiklik antidepresanlar (amitriptilin), birinci kuşak antihistaminikler (difenhidramin). Mesane detrüsör kasının muskarinik (M2/M3) reseptörlerini bloke ederek kasılmayı felç eder.\n2. **Sempatomimetikler (Alfa-Adrenerjik Agonistler):** Psödoefedrin (soğuk algınlığı ilaçları), efedrin. Mesane boynu ve prostatik kapsüldeki alfa-1 reseptörleri aşırı uyararak sfinkterik çıkım direncini artırır.\n3. **Opioid Analjezikler:** Morfin, fentanil; hem santral işeme refleksini baskılar hem de sfinkter spazmı yapar.\n\n> [!CRITICAL]\n> Hafif BPH'sı olan yaşlı bir hasta grip ilacı (psödoefedrin veya antihistaminik) aldığında birkaç saat içinde aniden glob vezikale (akut tam idrar retansiyonu) ile acile başvurabilir!",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_chain(
                "İlaç Kaynaklı Akut Üriner Retansiyon Kaskadı",
                [
                    "1. Soğuk Algınlığı İlacı Alımı: Psödoefedrin ve antihistaminik kombinasyonu tüketilmesi",
                    "2. Alfa-1 Reseptör Uyarımı: Prostat ve mesane boynu düz kaslarında şiddetli vazokonstriktif spazm",
                    "3. Antikolinerjik Blokaj: Detrüsör düz kasının M3 reseptörlerinin bloke edilerek kasılamaması",
                    "4. Çıkım Direnci Artışı ve Atoni: Direnç fırlarken pompalama gücünün sıfırlanması",
                    "5. Glob Vezikale: Mesanede 1000 mL üzerinde idrar birikmesi ve şiddetli supra-pubik ağrı"
                ]
            ),
            make_recall(
                "Prostatik düz kas tonusunu artırarak hafif BPH hastasında ani idrar retansiyonunu tetikleyen sempatomimetik ajan hangisidir?",
                "Psödoefedrindir (veya efedrin / alfa-adrenerjik agonistler).",
                "Grip ve soğuk algınlığı ilaçlarındaki dekonjestan etken madde"
            )
        ]
    })

    # Slide 19 - CHECKPOINT 2
    slides.append({
        "id": "k1-11-s19",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 2] Etiyolojik Düzeyler ve Patolojiler",
        "content": "Bu kontrol noktasında böbrekten üretraya kadar obstrüksiyona yol açan lezyonların haritasını pekiştiriyoruz:\n\n- **Böbrek Düzeyi:** UPJ darlığı, aberran damar kompresyonu, TCC/RCC, nefrolitiyazis ve papiller nekroz.\n- **Üreter Düzeyi:** Taşlar (en sık UVJ'de takılır), Ormond hastalığı (mediyale çekilen üreterler), gebelik (özellikle sağ taraf baskın), serviks kanseri basısı.\n- **Mesane ve Prostat:** BPH (en sık infravezikal neden), nörojenik mesane (detrüsör-sfinkter dissinerjisi), mesane tümörleri.\n- **Üretra:** Posterior üretral valv (erkek çocukta en sık konjenital), iatrojenik veya travmatik striktürler.\n- **İlaçlar:** Antikolinerjikler detrüsör atonisini, alfa-agonistler sfinkter spazmını tetikleyerek retansiyon yapar.\n\n==Klinik Çıkarım:== Yaş, cinsiyet ve anatomik darlıkların lokalizasyonu etiyolojik tanının en güvenilir anahtarıdır.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_table(
                ["Anatomik Bölge", "En Karakteristik Patoloji", "Fizyopatolojik Mekanizma"],
                [
                    [
                        {"text": "Böbrek Çıkımı (UPJ)", "isMasked": False, "hint": ""},
                        {"text": "Aberran damar veya intrinsik musküler darlık", "isMasked": True, "hint": "Konjenital geçiş bozukluğu"},
                        {"text": "Pelvis dilatasyonu ve kaliks hasarı", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Üreter Trasesi", "isMasked": False, "hint": ""},
                        {"text": "UVJ'de taş impaksiyonu veya gebelik basısı", "isMasked": True, "hint": "En dar geçit ve uterus mekaniği"},
                        {"text": "Akut kolik ve hidroüreter", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Üretra Seviyesi", "isMasked": False, "hint": ""},
                        {"text": "PUV (çocuk) veya BPH / Striktür (erişkin)", "isMasked": True, "hint": "Erkeklerde en tipik çıkım engelleri"},
                        {"text": "Bilateral hidroüreteronefroz ve mesane trabekülasyonu", "isMasked": False, "hint": ""}
                    ]
                ]
            ),
            make_recall(
                "İdrar akım engelinin 'Ormond hastalığı' olarak bilinen spesifik formu nedir?",
                "Retroperitoneal fibrozistir; üreterleri mediyale çeker ve dıştan sıkıştırır.",
                "Retroperitoneal idiyopatik sklerozan plak"
            )
        ]
    })

    # Slide 20
    slides.append({
        "id": "k1-11-s20",
        "title": "Pediatrik Üriner Obstrüksiyonlar: Konjenital Spektrum",
        "content": "Çocukluk çağında üriner obstrüksiyonlar çoğunlukla embriyolojik gelişim anomalilerine dayanır:\n\n- **Posterior Üretral Valv (PUV):**\n  - Erkek fetüslerde mezonefrik kanalın üretraya katılımındaki anomali sonucu oluşur.\n  - İntrauterin dönemde oligohidramniyos, pulmoner hipoplazi ve Potter sekansına yol açabilir.\n  - Mesane aşırı kalınlaşır, üreterler ileri derecede kıvrımlaşır (megaüreter) ve displazik böbrek hasarı gelişir.\n- **Üreterosel:** Distal üreterin intravezikal kısmının balonlaşması; özellikle duplikasyonlu (çift) toplayıcı sistemin üst pol üreterinde görülür.\n- **Prune-Belly Sendromu (Eagle-Barrett):** Abdominal kasların yokluğu, inmemiş testis ve toplayıcı sistemde masif dilatasyon ile karakterizedir.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_quiz(
                "Yenidoğan bir erkek bebekte prenatal USG'de bilateral masif hidroüreteronefroz, kalın duvarlı 'anahtar deliği' (keyhole) manzaralı mesane ve oligohidramniyos saptanıyor. En olası tanı hangisidir?",
                [
                    {"key": "A", "text": "Unilateral üreteropelvik darlık", "explanation": "A seçeneği yanlıştır: Tek taraflıdır, mesaneyi kalınlaştırmaz."},
                    {"key": "B", "text": "Posterior üretral valv (PUV)", "explanation": "B seçeneği doğrudur: Erkek bebekte infravezikal tıkanıklık, dilate posterior üretra ile mesanenin 'anahtar deliği' görüntüsü vermesi tipik PUV bulgusudur."},
                    {"key": "C", "text": "Basit renal kist", "explanation": "C seçeneği yanlıştır: Benign izole lezyondur."},
                    {"key": "D", "text": "Benign prostat hiperplazisi", "explanation": "D seçeneği yanlıştır: Yaşlılık patolojisidir."},
                    {"key": "E", "text": "Retroperitoneal fibrozis", "explanation": "E seçeneği yanlıştır: Erişkin otoimmün/inflamatuar tablodur."}
                ],
                "B"
            ),
            make_cloze(
                "Posterior üretral valvde ultrasonografide mesane ve dilate posterior üretranın oluşturduğu karakteristik görünüme anahtar deligi bulgusu adı verilir.",
                "anahtar deligi",
                "Keyhole manzarası"
            )
        ]
    })

    return slides
