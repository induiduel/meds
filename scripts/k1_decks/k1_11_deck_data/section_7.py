# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_7_slides():
    slides = []

    # Slide 61
    slides.append({
        "id": "k1-11-s61",
        "title": "Akut ve Kronik Obstrüksiyonun Karşılaştırmalı Kliniği",
        "content": "Üriner obstrüksiyonun klinik prezentasyonu tıkanıklığın gelişme hızına ve süresine göre birbirine tamamen zıt iki klinik tablo çizer:\n\n- **Akut Obstrüksiyon:** Genellikle üreter taşları veya pıhtı tıkanmasıyla aniden başlar. Toplayıcı sistemin ve böbrek kapsülünün ani gerilmesi çok şiddetli, kıvrandırıcı bir böğür (flank) ağrısına yol açar. Çölyak ganglion uyarımı nedeniyle tabloya bulantı, kusma ve paralitik ileus eşlik eder. Bakteriyel enfeksiyon binerse yüksek titremeli ateş ve taşikardi görülür.\n- **Kronik Obstrüksiyon:** Sinsi, yavaş ve ilerleyicidir. Toplayıcı sistem aylar içinde kademeli genişlediğinden renal kapsül gerilmez ve hasta genellikle tamamen ağrısızdır (asemptomatiktir). Bu nedenle kronik obstrüksiyonun tanısı son derece zordur; hastalar çoğunlukla üremi, hipertansiyon, halsizlik veya rastlantısal görüntülemeyle başvururlar.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_slider(
                "Akut ve Kronik Obstrüksiyon Kliniği Karşılaştırması",
                "Akut Obstrüksiyon",
                "Şiddetli kıvrandırıcı böğür ağrısı, bulantı, kusma, titreme; ani intrapelvik gerilme.",
                "Kronik Obstrüksiyon",
                "Genellikle tamamen ağrısız ve sinsi seyir; tanı zordur, üremi ve volüm yüklenmesiyle gelebilir."
            ),
            make_cloze(
                "Kronik üriner obstrüksiyon toplayıcı sistemin yavas genislemesi nedeniyle genellikle tamamen asemptomatik seyreder ve tanısı son derece zordur.",
                "asemptomatik seyreder",
                "Ağrısız ve sinsi gidişatı ifade eden klinik terim"
            )
        ]
    })

    # Slide 62
    slides.append({
        "id": "k1-11-s62",
        "title": "Akut Unilateral Obstrüksiyon: Renal Kolik ve Yansıma Paternleri",
        "content": "Akut tek taraflı üreter tıkanıklığının kardinal belirtisi renal kolik ağrısıdır. Bu ağrının temel patofizyolojik tetikleyicisi üreter duvarındaki aşırı intralüminal gerilim ve renal kapsülün gerilmesidir. Gerilme reseptörleri T10-L1 spinal segmentlerine giren sempatik lifler üzerinden merkezi sinir sistemine iletilir. Ağrı kosta-vertebral açıdan başlar ve tıkanıklığın anatomik seviyesine göre karakteristik bir yayılım gösterir:\n\n1. **Üst Üreter ve Pelvis:** Ağrı kosta-vertebral açıdan hipokondriyuma doğru yayılır.\n2. **Orta Üreter (Pelvik Kenar):** Ağrı alt karın kadranlarına ve McBurney noktasına yansıyarak akut apandisiti taklit edebilir.\n3. **Distal Üreter ve İntramural Bölge:** Ağrı kasık kanalına, uyluğun iç yüzüne, erkeklerde skrotum ve testise, kadınlarda labium majusa yansır; mesane irritasyonu nedeniyle pollaküri ve strangüri eklenir.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_table(
                ["Obstrüksiyon Seviyesi", "Ağrının Odak Noktası", "Yansıma Bölgesi"],
                [
                    [
                        {"text": "Pelvis ve Üst Üreter", "isMasked": False, "hint": ""},
                        {"text": "Kostovertebral açı ve böğür", "isMasked": True, "hint": "Sırt ve kaburga altı sınır"},
                        {"text": "Üst karın kadranı ve hipokondriyum", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Orta Üreter (İliak Çapraz)", "isMasked": False, "hint": ""},
                        {"text": "Pelvik brim ve alt kadran", "isMasked": True, "hint": "İliak damarların üst düzeyi"},
                        {"text": "İnguinal kanal ve McBurney noktası (apandisit taklidi)", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Distal İntramural Üreter (UVJ)", "isMasked": False, "hint": ""},
                        {"text": "Mesane tabanı ve pelvis", "isMasked": True, "hint": "Mesane duvarı girişi"},
                        {"text": "Skrotum, testis / labium majus ve uyluk içi", "isMasked": False, "hint": ""}
                    ]
                ]
            ),
            make_recall(
                "Distal intramural üreter taşında renal kolik ağrısının erkeklerde testise, kadınlarda labium majusa yansımasını sağlayan ortak dermatom segmenti hangisidir?",
                "T11-L1 spinal segmentleridir.",
                "Alt torakal ve üst lomber dermatomlar"
            )
        ]
    })

    # Slide 63
    slides.append({
        "id": "k1-11-s63",
        "title": "Akut Bilateral Obstrüksiyon ve Soliter Böbrek: Ani Anüri Acili",
        "content": "Klinik pratikte 24 saatlik idrar miktarının 50-100 ml'nin altına düşmesi 'anüri' olarak tanımlanır. Ani gelişen anüri, aksi kanıtlanana kadar **akut tam üriner sistem obstrüksiyonu** kabul edilmelidir. Prerenal şok veya glomerülonefritler oligüri yapabilse de, idrar çıkışının bıçak gibi aniden sıfıra inmesi neredeyse daima mekanik bir tıkanıklığı düşündürür. Bu durum iki klinik senaryoda gerçekleşir:\n\n1. **Akut Bilateral Tam Obstrüksiyon:** Her iki üreterin eş zamanlı taşla tıkanması veya retroperitoneal malign kitlelerin iki üreteri birden boğması.\n2. **Soliter Fonksiyonel Böbrekte Tek Taraflı Tıkanma:** Tek böbrekli (konjenital tek böbrek veya nefrektomili) bir hastada tek üreterin taş veya darlıkla tam tıkanması.\n\nBu tablo hızla potasyum yüksekliğine, pulmoner ödeme ve üremik ensefalopatiye yol açar; acil ürolojik dekompresyon şarttır.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_cloze(
                "Ani baslayan tam anüri tablosu, aksi kanıtlanana kadar bilateral ya da soliter böbrek üriner sistem obstrüksiyonu olarak kabul edilmelidir.",
                "soliter böbrek",
                "Tek bir fonksiyonel böbreğin bulunması durumu"
            ),
            make_quiz(
                "Daha önceden bilinen bir böbrek hastalığı olmayan 55 yaşında erkek hastada idrar çıkışı son 12 saattir tamamen duruyor (anüri) ve kreatinin 4.8 mg/dL ölçülüyor. Bu hastada ilk olarak ekarte edilmesi gereken patoloji hangisidir?",
                [
                    {"key": "A", "text": "Akut bilateral obstrüksiyon veya soliter böbrek mekanik obstrüksiyonu", "explanation": "A seçeneği doğrudur: Ani anüri aksi ispat edilene dek acil mekanik postrenal obstrüksiyondur."},
                    {"key": "B", "text": "Minimal lezyon hastalığına bağlı proteinüri", "explanation": "B seçeneği yanlıştır: Proteinüri ve ödem yapar, anüri yapmaz."},
                    {"key": "C", "text": "Böbrek taşlarının idrarı filtre etmesi", "explanation": "C seçeneği anlamsızdır."},
                    {"key": "D", "text": "Hipofiz adenomuna bağlı aşırı ADH salınımı", "explanation": "D seçeneği yanlıştır: Uygunsuz ADH anüri değil hiponatremi yapar."},
                    {"key": "E", "text": "Prostat bezinin tamamen atrofiye uğraması", "explanation": "E seçeneği yanlıştır: Atrofi obstrüksiyon yapmaz."},
                ],
                "A"
            )
        ]
    })

    # Slide 64
    slides.append({
        "id": "k1-11-s64",
        "title": "Kronik Obstrüksiyonun Sinsi Seyri ve Sistemik Üremi",
        "content": "Aylar veya yıllar içinde gelişen kronik supravezikal ya da infravezikal obstrüksiyonlar ağrı üretmedikleri için sinsi bir yıkım gerçekleştirirler. Hastalar sıklıkla ileri evrede üremik toksinlerin birikimine bağlı genel sistemik semptomlarla hekime gelir:\n\n- **Volüm Yüklenmesi:** Karın çevresinde artış (özellikle bilateral dev hidronefroza bağlı), pretibiyal ve ayak bileği ödemi, kilo artışı, akciğer konjesyonuna bağlı nefes darlığı ve ortopne.\n- **Üremik Toksisite:** Genel halsizlik, iştahsızlık, kilo kaybı, sabah bulantıları, yaygın kaşıntı ve dirençli baş ağrısı.\n- **İleri Nörolojik ve Hemostatik Bozulma:** Konsantrasyon güçlüğü, mental durum değişiklikleri, konfüzyon, üremik 'flapping tremor' (asteriksis) ve trombosit disfonksiyonuna bağlı gastrointestinal sistem kanamaları.\n\nBu aşamadaki hastaların serum üre ve kreatinin değerleri diyaliz sınırlarına ulaşmış olabilir.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_chain(
                "Kronik Obstrüksiyonun Sinsi Progresyonu",
                [
                    "1. Ağrısız Toplayıcı Dilatasyon: Kapsül gerilmeden pelvikaliksin aylar içinde büyümesi",
                    "2. Nefron İskemisi ve Skleroz: Tubulointerstisyel fibrozisle glomerül sayısının erimesi",
                    "3. Volüm ve Azotemi Birikimi: Sıvı yüklenmesi, ayak ödemi ve üre/kreatinin artışı",
                    "4. Terminal Üremi: Asteriksis, mental bulanıklık ve diyaliz gerektiren KBY tablosu"
                ]
            ),
            make_recall(
                "Kronik bilateral obstrüksiyonda üremik toksin birikimi sonucu ellerde ortaya çıkan istemsiz kaba düşme hareketine (flapping tremor) ne ad verilir?",
                "Asteriksis (asterixis).",
                "Metabolik ensefalopati tremoru"
            )
        ]
    })

    # Slide 65
    slides.append({
        "id": "k1-11-s65",
        "title": "Renal Kontrbalans Mekanizması: Hipertrofi ve Hipotrofi Dinamiği",
        "content": "Tek taraflı böbrek fonksiyon kaybı ve iyileşmesinde organlar arası dengeyi açıklayan temel fizyolojik kavrama 'Renal Kontrbalans' denir:\n\n- **Kompansatuar Hipertrofi:** Bir böbrek cerrahi olarak çıkarıldığında veya tek taraflı tam obstrüksiyonla fonksiyonunu yitirdiğinde, karşı sağlam böbrek organizmanın tüm filtrasyon yükünü tek başına üstlenir. Sağlam böbreğin nefronlarında hücresel protein sentezi artar; glomerüller ve tübüller belirgin şekilde büyüyerek **kompansatuar hipertrofiye** uğrar. Karşı böbrek tek başına iki böbreğin normal GFR kapasitesinin %70-80'ine kadar ulaşabilir.\n- **Renal Hipotrofi / Fonksiyonun Geri Çekilmesi:** Eğer obstrükte olan hasta böbreğin tıkanıklığı aylar sonra giderilirse veya hastaya yeni bir böbrek nakledilirse, kompanzasyon yapmış olan hipertrofik böbrek üzerindeki aşırı çalışma yükü kalkar; total renal fonksiyon normal fizyolojik seviyeye doğru aşağı çekilir (renal hipotrofi).",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_slider(
                "Renal Kontrbalansın İki Yönü Karşılaştırması",
                "Kompansatuar Hipertrofi",
                "Bir böbrek fonksiyonunu kaybettiğinde karşı sağlam böbreğin boyut ve filtrasyon kapasitesini artırmasıdır.",
                "Renal Hipotrofi",
                "Hasta böbreğin tıkanıklığı giderildiğinde hipertrofik böbreğin fonksiyonunun fizyolojik seviyeye geri çekilmesidir."
            ),
            make_cloze(
                "Bir böbrek obstrüksiyonla fonksiyonunu yitirdiğinde karşı sağlam böbreğin iş yükünü üstlenerek büyümesine kompansatuar hipertrofi denir.",
                "kompansatuar hipertrofi",
                "Tek kalan organın telafi edici büyüme süreci"
            )
        ]
    })

    # Slide 66
    slides.append({
        "id": "k1-11-s66",
        "title": "Obstrüktif Nefropatide Hipertansiyon Mekanizmaları",
        "content": "Üriner obstrüksiyon hem akut hem de kronik dönemde sekonder arteryel hipertansiyona neden olabilir. Altta yatan patofizyolojik mekanizma obstrüksiyonun tek taraflı veya iki taraflı olmasına göre farklılık gösterir:\n\n1. **Tek Taraflı Obstrüksiyon:** Obstrükte böbrekte renal perfüzyonun ve afferent arteriyol akımının azalması jukstaglomerüler aparatı uyarır. Yüksek miktarda **renin** salgılanır; Renin-Anjiyotensin-Aldosteron Sistemi (RAAS) aşırı aktive olarak Anjiyotensin II vazokonstriksiyonu ile 'renin bağımlı vazokonstriktif hipertansiyon' tablosu oluşturur.\n2. **İki Taraflı (Bilateral) Obstrüksiyon:** Her iki böbrekte filtrasyon düştüğü için temel mekanizma su ve sodyumun vücutta birikmesidir ('volüm bağımlı hipertansiyon'). Aşırı intravasküler volüm genişlemesi kan basıncını yükseltir.\n\nKritik klinik gözlem: Obstrüksiyon cerrahi veya drenajla açıldığında, gelişen natriürez ve diürez ile birlikte hipertansiyon hızla geriler ve kan basıncı normale döner.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_table(
                ["Obstrüksiyon Tipi", "Temel Hipertansiyon Mekanizması", "Dekompresyon Yanıtı"],
                [
                    [
                        {"text": "Tek Taraflı (Unilateral)", "isMasked": False, "hint": ""},
                        {"text": "İskemik böbrekten yüksek renin salınımı ve RAAS aktivasyonu", "isMasked": True, "hint": "Vazokonstriktör hormon artışı"},
                        {"text": "Renin düşüşü ile kan basıncı geriler", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "İki Taraflı (Bilateral)", "isMasked": False, "hint": ""},
                        {"text": "Masif su ve sodyum retansiyonuna bağlı hipervolemi", "isMasked": True, "hint": "Vücutta sıvı ve tuz birikmesi"},
                        {"text": "Postobstrüktif diürezle volüm atılınca hızla düzelir", "isMasked": False, "hint": ""}
                    ]
                ]
            ),
            make_recall(
                "Tek taraflı üreter obstrüksiyonunda arteriyel hipertansiyonu tetikleyen temel endokrin sistem hangisidir?",
                "Renin-anjiyotensin-aldosteron sistemidir (RAAS).",
                "Jukstaglomerüler aparattan salınan enzim yolağı"
            )
        ]
    })

    # Slide 67
    slides.append({
        "id": "k1-11-s67",
        "title": "Enfekte Obstrüksiyon: Piyonefroz, Ürosepsis ve Acil Drenaj",
        "content": "Ürolojideki en ölümcül klinik acil, obstrükte bir toplayıcı sistemin bakterilerle enfekte olmasıdır. Toplayıcı sistem staz halindeyken bakteriler hızla çoğalır; lökosit infiltrasyonu ile toplayıcı sistem lümeni püy ile dolarak böbrek adeta içi iltihap dolu kapalı bir apse kesesine dönüşür (piyonefroz). İntrapelvik hidrostatik basıncın yüksekliği nedeniyle bakteriler ve bakteriyel endotoksinler (LPS), forniks mikro-yırtıklarından ve pyelovenöz/pyelolenfatik geri akım yollarından dakikalar içinde doğrudan kana karışır. Hastada kontrolsüz titreme, yüksek ateş (>38.5°C), hipotansiyon, taşikardi ve lökositoz ile karakterize **üroseptik şok** tablosu patlak verir. Bu durumda tek başına intravenöz antibiyotik vermek yetersizdir ve hastayı kurtarmaz; tıkanıklık acilen perkütan nefrostomi veya JJ stent ile dekomprese edilip basınç düşürülmelidir.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_branching(
                "65 yaşında kadın hasta, sağ yan ağrısı, 39.5°C ateş, titreme, tansiyon 80/50 mmHg ve konfüzyon ile getiriliyor. USG'de sağ üreter üst uçta 12 mm taş ve kalikslerde yoğun püy partikülleri içeren ağır hidronefroz (piyonefroz) saptanıyor.",
                "Bu aşamada hastanın hayatını kurtaracak en acil ve zorunlu tedavi yaklaşımı nedir?",
                [
                    {
                        "text": "Acil perkütan nefrostomi veya JJ stent ile enfekte toplayıcı sistemin derhal dekomprese edilmesi ve IV geniş spektrumlu antibiyotik başlanması.",
                        "isCorrect": True,
                        "feedback": "Doğrudur. Tıkanmış ve enfekte sistem kapalı bir apsedir; drenaj yapılmaksızın verilen antibiyotik dokuya ulaşamaz ve sepsis mortal seyreder."
                    },
                    {
                        "text": "Yalnızca oral analjezik verip taşın kendiliğinden düşmesini beklemek.",
                        "isCorrect": False,
                        "feedback": "Yanlıştır. Piyonefroz ve septik şok tablosunda bekleme ölümcüldür."
                    },
                    {
                        "text": "Aynı seansta hemen açık radikal nefrektomi ile böbreği çıkarmak.",
                        "isCorrect": False,
                        "feedback": "Yanlıştır. Şoktaki hastada elektif cerrahi kontrendikedir; ilk adım minimal invaziv acil drenajdır."
                    }
                ]
            ),
            make_cloze(
                "Obstrükte toplayıcı sistemin püy ile dolması sonucu olusan piyonefroz tablosu acil dekompresyon gerektiren ürolojik bir acildir.",
                "piyonefroz",
                "Böbrek toplayıcı sisteminin cerahatle dolması durumu"
            )
        ]
    })

    # Slide 68
    slides.append({
        "id": "k1-11-s68",
        "title": "Alt Üriner Sistem Semptomları (LUTS): Depolama vs Boşaltım",
        "content": "İnfravezikal obstrüksiyonu olan hastalarda alt üriner sistem semptomları (LUTS) semptomların ortaya çıktığı miksiyon fazına göre iki ana gruba ayrılır:\n\n1. **Depolama (İrritatif) Semptomları:** Mesane dolum fazında mukoza konjesyonu ve detrüsör aşırı duyarlılığına bağlıdır. Gündüz sık idrara çıkma (pollaküri), gece idrara kalkma (noktüri), ani sıkışma hissi (urgency) ve sıkışma tipi idrar kaçırmadır (urge inkontinans).\n2. **Boşaltım (Obstrüktif) Semptomları:** Miksiyon fazında mekanik çıkım direncine karşı ortaya çıkar. İdrar başlatırken bekleme (hesitancy), idrar akım hızında zayıflama (weak stream), çatallı işeme, kesik kesik işeme (intermittency), ıkınarak işeme ve işeme sonunda damlama (terminal dribbling).\n\nObstrüksiyon ilerledikçe boşaltım semptomları derinleşir ve mesanede rezidüel idrar birikimi artar.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_table(
                ["Semptom Grubu", "Temel Mekanizma", "Karakteristik Örnekler"],
                [
                    [
                        {"text": "Depolama (İrritatif)", "isMasked": False, "hint": ""},
                        {"text": "Mukozal ödem, gerilme ve detrüsör irritabilitesi", "isMasked": True, "hint": "Dolum esnasındaki hassasiyet"},
                        {"text": "Pollaküri, noktüri, urgency, urge inkontinans", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Boşaltım (Obstrüktif)", "isMasked": False, "hint": ""},
                        {"text": "Lümendeki fiziksel direnç ve detrüsör yorgunluğu", "isMasked": True, "hint": "İdrar çıkış kanalındaki mekanik blokaj"},
                        {"text": "Hesitancy, zayıf akım, kesik işeme, terminal damlama", "isMasked": False, "hint": ""}
                    ]
                ]
            ),
            make_recall(
                "İdrar yapmaya başlarken zorlanma ve bekleme şikayetini tanımlayan boşaltım fazı obstrüktif semptomu hangisidir?",
                "Hesitansidir (hesitancy).",
                "İşemeyi başlatma gecikmesi terimi"
            )
        ]
    })

    # Slide 69 (CHECKPOINT 7)
    slides.append({
        "id": "k1-11-s69",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 7] Klinik Tablo, Renal Kolik, Anüri ve Renal Kontrbalans",
        "content": "Üriner obstrüksiyonun klinik prezentasyonunun ana hatları:\n\n1. **Klinik Profil:** Akut obstrüksiyon şiddetli renal kolik ağrısı ve bulantı ile gelirken; kronik obstrüksiyon asemptomatik, sinsi seyreder ve üremi ile başvurur.\n2. **Kritik Acil:** Ani gelişen anüri aksi kanıtlanana kadar bilateral veya soliter böbrek tam mekanik obstrüksiyonudur.\n3. **Renal Kontrbalans:** Bir böbrek fonksiyonunu yitirdiğinde sağlam böbrek kompansatuar hipertrofiye uğrar; hasta böbrek açıldığında aşırı fonksiyon normal düzeye geri çekilir (hipotrofi).\n4. **Hipertansiyon:** Tek taraflıda renin bağımlı, iki taraflıda volüm bağımlıdır; dekompresyon sonrası diürezle geriler.\n5. **Piyonefroz:** Enfekte obstrüksiyon üroseptik şok riskidir; tek başına antibiyotik yetmez, acil drenaj hayat kurtarır.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_quiz(
                "Üriner obstrüksiyonda gelişen hipertansiyonun fizyopatolojik mekanizmalarıyla ilgili hangisi DOĞRUDUR?",
                [
                    {"key": "A", "text": "Tek taraflı obstrüksiyonda renin artışı, bilateral obstrüksiyonda su ve tuz retansiyonu hakimdir.", "explanation": "A seçeneği DOĞRUDUR: Unilateralde iskemiye bağlı RAAS aktivasyonu, bilateralde ise volüm yüklenmesi hipertansiyon üretir."},
                    {"key": "B", "text": "Obstrüksiyon cerrahi olarak açılsa dahi hipertansiyon asla düzelmez.", "explanation": "B seçeneği yanlıştır: Obstrüksiyon giderilince diürezle tansiyon düzelir."},
                    {"key": "C", "text": "Bilateral obstrüksiyonda böbrekler tüm tuzu idrarla atarak hipotansiyon yapar.", "explanation": "C seçeneği yanlıştır: Bilateral obstrüksiyonda su ve tuz tutulur, tansiyon yükselir."},
                    {"key": "D", "text": "Renin salgısı obstrükte böbrekte tamamen sıfıra iner.", "explanation": "D seçeneği yanlıştır: Tek taraflı tıkanıklıkta renin salgısı tavan yapar."},
                    {"key": "E", "text": "Hipertansiyon yalnızca eksternal üretral darlıklarda görülür.", "explanation": "E seçeneği yanlıştır: Tüm seviyelerdeki obstrüksiyonlar hipertansiyon yapabilir."}
                ],
                "A"
            ),
            make_cloze(
                "Akut toplayıcı sistem gerilmesiyle ortaya cıkan kıvrandırıcı renal kolik ağrısı T10-L1 dermatomlarına yansır.",
                "renal kolik ağrısı",
                "Karakteristik üreter taşı ağrısı tanımlaması"
            )
        ]
    })

    # Slide 70
    slides.append({
        "id": "k1-11-s70",
        "title": "Fizik Muayene Bulguları ve Laboratuvar Analizi",
        "content": "Obstrüktif üropatili bir hastanın fizik muayenesinde ve laboratuvar testlerinde spesifik ipuçları aranmalıdır:\n\n- **Fizik Muayene:** Karın ve böğür palpasyonunda kosta-vertebral açı hassasiyeti (KVAH / Giordani pozitifliği), ileri hidronefrotik böbrek kitlesi veya distandü mesane (glob vezikale) ele gelebilir. Bilateral veya kronik olgularda hacim yüklenmesi belirtileri (pretibiyal gode bırakan ödem, asit, boyun venöz dolgunluğu, akciğerde raller ve hipertansiyon) aranır.\n- **Laboratuvar:** Serum biyokimyasında üre, kreatinin ve ürik asit yüksekliği (azotemi) ile hiperkalemi ve metabolik asidoz izlenir. Tam idrar analizinde mikroskobik veya makroskopik **hematüri** (özellikle taş ve tümörlerde), enfeksiyon varsa piyüri ve lökositoz görülür. İdrar mikroskopisinde kristaller (ürolitiyazis kanıtı), tübüler epitel hücre silendirleri ve geniş bal mumu silendirleri (kronik böbrek yetmezliği göstergesi) saptanabilir.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran)",
        "elements": [
            make_table(
                ["İnceleme Parametresi", "Bulgu", "Klinik Yorum"],
                [
                    [
                        {"text": "Böğür Muayenesi", "isMasked": False, "hint": ""},
                        {"text": "Kostovertebral açı hassasiyeti (Giordani testi)", "isMasked": True, "hint": "Böbrek lojuna perküsyonla ağrı uyandırma"},
                        {"text": "Akut gerilme ve enfeksiyon bulgusu", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "İdrar Sedimenti", "isMasked": False, "hint": ""},
                        {"text": "Hematüri, kristalüri ve piyüri", "isMasked": True, "hint": "Mikroskobik idrar şekilli elemanları"},
                        {"text": "Taş, tümör veya süperpoze enfeksiyon göstergesi", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Serum Biyokimyası", "isMasked": False, "hint": ""},
                        {"text": "Üre, kreatinin yüksekliği ve hiperkalemi", "isMasked": True, "hint": "Azotemi ve elektrolit birikim belirteçleri"},
                        {"text": "Filtrasyon çöküşü ve renal yetmezlik derecesi", "isMasked": False, "hint": ""}
                    ]
                ]
            ),
            make_recall(
                "Akut toplayıcı sistem gerilmesinde sırt bölgesinde böbrek lojuna yumruk vurulduğunda şiddetli ağrı duyulması testine ne ad verilir?",
                "Kosta-vertebral açı hassasiyeti (KVAH / Giordani belirtisi).",
                "Klasik böbrek perküsyon muayene bulgusu"
            )
        ]
    })

    return slides
