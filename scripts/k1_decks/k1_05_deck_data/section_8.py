"""
Bölüm 8: Nekroz-Apoptoz Karşılaştırması ve Diğer Hücre Ölümü Biçimleri
Adımlar: 71 - 80
Checkpoint: Adım 79 (3 Akıl Kartı)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_8_slides():
    slides = []

    # ADIM 71
    slides.append({
        "slideNumber": 71,
        "title": "Nekroz ile Apoptozun Karşılaştırma Matrisi: Temel Farklılıklar",
        "subtitle": "Hücre boyutu, membran durumu, çekirdek akıbeti ve enerji ihtiyacının kesin ayrımı",
        "badge": "Karşılaştırma",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Hücre ölümünün iki ana kutbu olan nekroz ve apoptoz, hücresel biyolojinin en temel karşılaştırma "
            "eksenini oluşturur. Bu ayrım patoloji sınavlarının vazgeçilmez temel taşıdır.\n\n"
            "Nekroz; şiddetli hipoksi, toksin veya iskemi sonucu gelişen, enerji (ATP) gerektirmeyen, hücrenin "
            "şişerek patladığı, membran bütünlüğünün yok olduğu ve çevre dokuda yoğun inflamasyon yaratan kaotik bir ölümdür.\n\n"
            "> [SINAV SPOTU] Apoptoz ise; fizyolojik veya patolojik olabilen, aktif ATP gerektiren, hücrenin büzüşüp "
            "küçüldüğü, membran bütünlüğünü koruyan ve ASLA inflamasyon oluşturmayan programlı bir intihardır!\n\n"
            "Nekrozda nükleus piknoz, karyoreksis ve karyolizis gösterirken; apoptozda nükleozom boyutunda kırılma izlenir."
        ),
        "medicalTerms": [
            {"term": "Onkozis", "explanation": "Nekroz öncesinde hücrenin su alarak şişmesi olayı."},
            {"term": "Hücresel İntihar", "explanation": "Apoptozun hücresel ATP harcayarak kendi genetik infazını gerçekleştirmesi."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Nekroz enerji (ATP) bağımsızdır; Apoptoz enerji (ATP) bağımlıdır.",
            "📌 [SINAV SPOTU] Nekrozda hücre şişer (onkozis); Apoptozda hücre küçülür ve büzüşür (shrinkage).",
            "📌 [SINAV SPOTU] Nekrozda membran parçalanır ve inflamasyon vardır; Apoptozda membran sağlam kalır ve inflamasyon yoktur."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Enerji Paradoksu", "desc": "Nekrozda ATP tükenmiştir; apoptoz kaspazlar için ATP harcar.", "isKey": True},
                {"title": "İnflamasyon Ayrımı", "desc": "Nekrozda nötrofil istilası, apoptozda sessiz makrofaj temizliği.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Parametre", "Nekroz", "Apoptoz"],
                [
                    [("Hücre Boyutu", False, ""), ("Büyümüş / Şişmiş (Onkozis)", True, "Nekroz hücre hacmi"), ("Azalmış / Büzüşmüş (Shrinkage)", False, "")],
                    [("Enerji (ATP)", False, ""), ("Gerektirmez (Enerji bağımsız)", True, "Nekroz ATP ihtiyacı"), ("ATP gerektirir (Enerji bağımlı)", False, "")],
                    [("Plazma Zarı", False, ""), ("Bozulmuş / Parçalanmış", True, "Nekroz zar durumu"), ("Korunmuş (Fosfatidilserin dışta)", False, "")],
                    [("İnflamasyon", False, ""), ("Sık ve Belirgin", True, "Nekroz yangısal yanıtı"), ("Yok veya Minimal", False, "")],
                    [("Biyolojik Rol", False, ""), ("Daima Patolojik", True, "Nekroz oluşum doğası"), ("Çoğunlukla Fizyolojik (bazen patolojik)", False, "")]
                ]
            ),
            make_cloze(
                "Nekroz hücresel enerji gerektirmezken apoptoz aktif olarak ATP bağımlı şekilde yürütülür.",
                "ATP bağımlı",
                "Apoptozun enerji gereksinimi durumu"
            )
        ]
    })

    # ADIM 72
    slides.append({
        "slideNumber": 72,
        "title": "Nekroptoz: Nekroz ile Apoptozun Programlı Hibriti",
        "subtitle": "Kaspaz bağımsız, RIPK1-RIPK3-MLKL kompleksi ile yürütülen düzenlenmiş nekroz",
        "badge": "Nekroptoz",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Geleneksel olarak nekrozun tamamen rastgele, apoptozun ise programlı olduğu kabul edilirdi. "
            "Ancak son yıllarda keşfedilen 'Nekroptoz' (Necroptosis), bu iki kavramı birleştiren devrimci bir hücre ölümüdür.\n\n"
            "Nekroptoz morfolojik olarak tıpkı klasik nekroza benzer: Hücre şişer, plazma zarı patlar, hücre içeriği "
            "dokuya sızar ve belirgin inflamasyon oluşur.\n\n"
            "> [SINAV SPOTU] Ancak nekroptozun mekanizması apoptoz gibi genetik olarak PROGRAMLIDIR! En kritik özelliği "
            "ise 'KASPAZ-BAĞIMSIZ' olmasıdır; Kaspaz-8 bloke olduğunda veya inaktifken devreye girer!\n\n"
            "Özellikle virüsler kaspazları bloke ettiğinde, konak hücresi nekroptoz yolunu açarak virüsün çoğalmasını "
            "engellemek için kendini feda eder."
        ),
        "medicalTerms": [
            {"term": "Nekroptoz", "explanation": "Programlı ve genetik sinyalle başlayan ancak nekroz morfolojisi ve inflamasyonla sonuçlanan kaspaz-bağımsız ölüm."},
            {"term": "Düzenlenmiş Nekroz", "explanation": "İntraselüler kinaz kompleksleri (nekrozom) tarafından yönetilen kontrollü nekroz formu."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Nekroptoz morfolojik olarak nekroza benzer (şişme, lizis, inflamasyon), ancak genetik olarak programlıdır.",
            "📌 [SINAV SPOTU] Nekroptoz KASPAZ-BAĞIMSIZDIR; Kaspaz-8 inaktifken devreye girer.",
            "📌 [SINAV SPOTU] TNF sinyalleri ile tetiklenebilir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Hibrit Özellik", "desc": "Apoptoz gibi programlı sinyal, nekroz gibi zarlı patlama ve yangı.", "isKey": True},
                {"title": "Kaspaz Bağımsızlığı", "desc": "Kaspaz-8 inhibe olduğunda nekroptoz kaskadının serbest kalması.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_micro_quiz(
                "Morfolojik olarak hücre şişmesi, plazma zarı yırtılması ve inflamasyonla seyreden (nekroz benzeri) ancak genetik olarak programlanmış ve Kaspaz-bağımsız çalışan hücre ölümü hangisidir?",
                {
                    "A": "Klasik Apoptoz",
                    "B": "Nekroptoz",
                    "C": "Otofaji",
                    "D": "Kazeöz nekroz",
                    "E": "Fibrinoid nekroz"
                },
                "B",
                {
                    "A": "Apoptoz kaspaz bağımlıdır ve membran sağlam kalır.",
                    "B": "Doğru cevap B'dir: Nekroptoz programlı nekrozdur ve kaspaz bağımsızdır.",
                    "C": "Otofaji lizozomal sindirim ve hayatta kalma yoludur.",
                    "D": "Kazeöz nekroz tüberkülozdadır.",
                    "E": "Fibrinoid nekroz damarlardadır."
                }
            ),
            make_cloze(
                "Nekroz benzeri morfolojiye sahip olan ancak kaspazlardan bağımsız ve programlı yürütülen hücre ölümüne nekroptoz denir.",
                "nekroptoz",
                "Programlı nekroz hibrit hücre ölümü adı"
            )
        ]
    })

    # ADIM 73
    slides.append({
        "slideNumber": 73,
        "title": "Nekroptozun Moleküler Düzeneği: RIPK1, RIPK3 ve MLKL (Nekrozom)",
        "subtitle": "Kaspaz-8'in yokluğunda kinazların fosforillenmesi ve zarın delinmesi",
        "badge": "Nekrozom",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Nekroptozun moleküler koreografisi TNFR1 reseptörünün uyarılmasıyla başlar. Normal koşullarda reseptör "
            "altında Kaspaz-8 aktive olur ve 'RIPK1' ile 'RIPK3' kinazlarını keserek parçalar (böylece nekroptoz engellenir).\n\n"
            "Ancak ortamda viral kaspaz inhibitörleri varsa veya Kaspaz-8 bloke edilmişse, RIPK1 ve RIPK3 kesilemez. "
            "RIPK1 ve RIPK3 birbirini çapraz fosforilleyerek 'Nekrozom' (Necrosome) kompleksini kurar.\n\n"
            "> [SINAV SPOTU] Aktifleşen RIPK3 kinazı, sitoplazmik bir psödokinaz olan 'MLKL'yi (Mixed Lineage Kinase "
            "Domain-Like) fosforiller. Fosforillenen MLKL oligomerleşip plazma zarına göç eder ve zarda gözenekler açarak "
            "hücreyi patlatır!\n\n"
            "Bu süreç akut pankreatit, miyokard enfarktüsü reperfüzyonu ve septik şokta doku harabiyetini yönetir."
        ),
        "medicalTerms": [
            {"term": "RIPK1 / RIPK3", "explanation": "Reseptör Etkileşimli Protein Kinaz 1 ve 3; nekrozom kompleksini oluşturan ana kinazlar."},
            {"term": "MLKL", "explanation": "RIPK3 ile fosforillenip plazma zarına saplanarak por açan nekroptoz efektör proteini."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Nekroptoz sinyal kaskadı: RIPK1 -> RIPK3 -> MLKL oligomerizasyonu.",
            "📌 [SINAV SPOTU] MLKL plazma membranına saplanarak delikler açar ve hücreyi patlatır.",
            "📌 [SINAV SPOTU] Kaspaz-8 aktifken RIPK1/RIPK3'ü parçalayarak nekroptozu baskılar."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Nekrozom Kinazları", "desc": "RIPK1 ve RIPK3'ün kaspaz-8 yokluğunda fosforillenmesi.", "isKey": True},
                {"title": "MLKL Delgisi", "desc": "Fosforillenmiş MLKL oligomerlerinin plazma zarını yırtması.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_causal_chain(
                "Nekroptoz Moleküler İnfaz Zinciri",
                [
                    "1. TNF Uyarısı: TNF ligandı TNFR1 ölüm reseptörüne bağlanır.",
                    "2. Kaspaz-8 Blokajı: Kaspaz-8 inaktif olduğundan RIPK1 ve RIPK3 kesilip parçalanamaz.",
                    "3. Nekrozom Oluşumu: RIPK1 ve RIPK3 birbirini fosforilleyerek nekrozom kompleksini kurar.",
                    "4. MLKL Fosforilasyonu: RIPK3 MLKL proteinini fosforilleyerek oligomerleşmesini tetikler.",
                    "5. Zar Rüptürü: MLKL oligomerleri plazma zarına saplanıp porlar açar ve hücreyi nekrozla patlatır."
                ]
            ),
            make_cloze(
                "Nekroptozda RIPK3 kinazı tarafından fosforillenerek plazma zarına göç eden ve zarı delen molekül MLKL proteinidir.",
                "MLKL",
                "Nekroptozun zarı delen efektör proteini kısaltması"
            )
        ]
    })

    # ADIM 74
    slides.append({
        "slideNumber": 74,
        "title": "Piroptoz: İnflamozom, Ateş ve Gazdermin D ile Patlayan Hücreler",
        "subtitle": "Hücre içi mikroplara karşı Kaspaz-1 aktivasyonu ve IL-1beta salınımı ile seyreden ölüm",
        "badge": "Piroptoz",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Adını Yunanca 'pyro' (ateş) ve 'ptosis' (düşme) kelimelerinden alan 'Piroptoz' (Pyroptosis), "
            "yüksek ateş ve şiddetli inflamasyon ile karakterize özel bir programlı hücre ölümüdür.\n\n"
            "Genellikle Salmonella, Shigella ve Legionella gibi hücre içine yerleşen bakterilerle enfekte olmuş "
            "makrofajlarda görülür. Hücre içi patojen sensörleri (NLRP3 vb.) 'İnflamozom' kompleksini kurar.\n\n"
            "> [SINAV SPOTU] İnflamozom, apoptotik kaspazları değil, 'Kaspaz-1'i aktive eder! Kaspaz-1 ise pro-IL-1β ve "
            "pro-IL-18'i keserek aktif sitokinlere dönüştürür ve 'Gazdermin D' proteinini ikiye böler!\n\n"
            "Gazdermin D'nin N-terminal parçası plazma zarına saplanarak delikler açar; hücre şişip patlarken ortama "
            "yoğun IL-1 salınır ve sistemik yüksek ateş tetiklenir."
        ),
        "medicalTerms": [
            {"term": "Piroptoz", "explanation": "İnflamozom ve Kaspaz-1 aktivasyonu ile gazdermin D porları oluşturan, IL-1 salınımlı ateşli hücre ölümü."},
            {"term": "Gazdermin D", "explanation": "Kaspaz-1 tarafından kesildiğinde plazma zarında porlar açarak piroptoza yol açan por yapıcı protein."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Piroptoz: İnflamozom aktivasyonu + KASPAZ-1 + IL-1 salınımı + ATEŞ ve inflamasyon.",
            "📌 [SINAV SPOTU] Hücre zarında delikleri açan efektör protein 'Gazdermin D'dir.",
            "📌 [SINAV SPOTU] Klasik apoptoz kaspazları (Kaspaz-3/8/9) değil, inflamatuar kaspaz (KASPAZ-1) çalışır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "İnflamozom Motoru", "desc": "NLRP3 sensörünün Kaspaz-1'i devreye sokması.", "isKey": True},
                {"title": "Ateş ve Gazdermin", "desc": "IL-1beta salınımı ile yüksek ateş ve Gazdermin D delikleri.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Özellik", "Apoptoz", "Piroptoz"],
                [
                    [("Sorumlu Kaspaz", False, ""), ("Kaspaz-3, -8, -9 (Apoptotik)", True, "Apoptoz kaspaz grubu"), ("Kaspaz-1, Kaspaz-4, -5 (İnflamatuar)", False, "")],
                    [("İnflamasyon ve Ateş", False, ""), ("İnflamasyon YOK, ateş YOK", True, "Apoptozun sessiz doğası"), ("Şiddetli inflamasyon ve YÜKSEK ATEŞ", False, "")],
                    [("Membran Akıbeti", False, ""), ("Bütünlüğü korunur, cisimcikler oluşur", True, "Apoptoz zar yapısı"), ("Gazdermin D ile delinir ve patlar", False, "")]
                ]
            ),
            make_cloze(
                "Piroptoz sürecinde inflamozom kompleksi tarafından aktive edilen ve IL-1beta salınımını sağlayan enzim kaspaz-1 enzimidir.",
                "kaspaz-1",
                "İnflamatuar kaspaz numarası"
            )
        ]
    })

    # ADIM 75
    slides.append({
        "slideNumber": 75,
        "title": "Ferroptoz: Demir Bağımlı Lipid Peroksidasyon Krizi",
        "subtitle": "Glutatyon peroksidaz 4 (GPX4) iflası ve membran fosfolipidlerinin alev alması",
        "badge": "Ferroptoz",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Hücre ölümünün en genç ve en popüler araştırma alanlarından biri 'Ferroptoz'dur (Ferroptosis). "
            "Bu süreç hücre içindeki serbest demir (Fe²⁺) iyonlarının birikmesiyle tetiklenen son derece özgün bir ölümdür.\n\n"
            "Normalde hücre zarı fosfolipidlerini oksidasyondan koruyan ana enzim 'Glutatyon Peroksidaz 4'tür (GPX4). "
            "GPX4 çalışabilmek için hücreye sistin girişi sağlayan 'Sistem Xc⁻' antiporterına ve glutatyona (GSH) muhtaçtır.\n\n"
            "> [SINAV SPOTU] Sistin girişi durduğunda veya GPX4 inaktive olduğunda, hücre içi serbest demir Fenton "
            "reaksiyonuyla kontrolsüz serbest radikal üretir. Bu radikaller plazma zarı lipidlerini yakıp yıkar "
            "(Demir bağımlı lipid peroksidasyonu)!\n\n"
            "Ferroptozda apoptoz morfolojisi görülmez; en belirgin organel bulgusu mitokondrilerin küçülmesi ve "
            "kristalarının kaybolmasıdır. İnme, Parkinson ve kanser kemoterapisi araştırmalarında merkezdedir."
        ),
        "medicalTerms": [
            {"term": "Ferroptoz", "explanation": "Hücre içi serbest demir fazlalığı ve GPX4 yetmezliği sonucu gelişen demir bağımlı lipid peroksidasyonu ölümü."},
            {"term": "GPX4 (Glutatyon Peroksidaz 4)", "explanation": "Zar fosfolipid hidroperoksitlerini indirgeyerek ferroptozu engelleyen anahtar antioksidan enzim."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Ferroptoz: Demir (Fe²⁺) bağımlı lipid peroksidasyonu ile karakterizedir.",
            "📌 [SINAV SPOTU] Glutatyon peroksidaz 4 (GPX4) kaybı veya sistin taşınmasının bozulması tetikler.",
            "📌 [SINAV SPOTU] Kaspazlardan bağımsızdır; elektron mikroskobunda mitokondriler küçülür ve kristalar silinir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Demir Katalizi", "desc": "Fe2+ iyonlarının Fenton reaksiyonuyla membran lipitlerini peroksitlemesi.", "isKey": True},
                {"title": "GPX4 Çöküşü", "desc": "Glutatyon peroksidaz 4 durduğunda hücrenin kaçınılmaz ölümü.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_active_recall(
                "Ferroptoz hücre ölümünün en temel biyokimyasal mekanizması ve bu süreçte koruyucu olan ana enzim hangisidir?",
                "Temel mekanizma demir (Fe²⁺) bağımlı lipid peroksidasyonudur; koruyucu ana enzim Glutatyon Peroksidaz 4'tür (GPX4)."
            ),
            make_cloze(
                "Hücre içi serbest demir iyonlarının lipid peroksidasyonunu tetiklemesiyle gelişen programlı hücre ölümüne ferroptoz denir.",
                "ferroptoz",
                "Demir bağımlı hücre ölümü terimi"
            )
        ]
    })

    # ADIM 76
    slides.append({
        "slideNumber": 76,
        "title": "Otofaji (Kendi Kendini Yeme): Temel Hayatta Kalma Mekanizması",
        "subtitle": "Açlık ve besin yoksunluğunda hücresel organellerin lizozomlarda sindirilip geri dönüştürülmesi",
        "badge": "Otofaji",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Hücre hasarı başlığının son büyük konusu 'Otofaji'dir (Autophagy / Kendi Kendini Yeme). "
            "Otofaji temelde bir hücre ölümü biçimi DEĞİL; hücrenin besin yoksunluğu ve açlık gibi şiddetli stres "
            "durumlarında hayatta kalabilmek için geliştirdiği bir kurtarma ve geri dönüşüm mekanizmasıdır.\n\n"
            "Besin kıtlığı baş gösterdiğinde hücre sitoplazmasındaki yaşlı veya hasarlı organelleri (mitokondri, ER) "
            "kendi lizozomlarında sindirerek aminoasit, yağ asidi ve enerji elde eder.\n\n"
            "> [SINAV SPOTU] Hücre stres altındayken kendi kendini kısmen yiyerek metabolik yakıt üretir ve canlı kalır!\n\n"
            "Ancak besin yoksunluğu çok uzar veya kontrolsüz aşırı otofaji gelişirse, hücre tüm yapılarını tüketerek "
            "otofajik hücre ölümüne sürüklenebilir."
        ),
        "medicalTerms": [
            {"term": "Otofaji (Kendi Kendini Yeme)", "explanation": "Hücrenin sitoplazmik içeriklerini ve organellerini çift zarlı veziküllere alıp lizozomda sindirmesi süreci."},
            {"term": "Hücresel Katabolizma", "explanation": "Metabolik enerji sağlamak amacıyla hücresel makromoleküllerin parçalanması."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Otofaji temelde bir hayatta kalma (survival) mekanizmasıdır.",
            "📌 [SINAV SPOTU] Besin yoksunluğunda hücresel yapıları sindirip geri dönüştürerek hücreye enerji sağlar.",
            "📌 [SINAV SPOTU] Kontrolsüz veya aşırı olduğunda hücre ölümüne de yol açabilir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Geri Dönüşüm Sistemi", "desc": "Hücrenin kendi çöplerini ve yaşlı organellerini yakıta çevirmesi.", "isKey": True},
                {"title": "Hayatta Kalma vs Ölüm", "desc": "Öncelikle kurtarma adaptasyonu, aşırı durumda son çare ölüm.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "Otofaji Fizyolojik Rolü: Sağkalım vs Ölüm",
                "Fizyolojik Rolü (Sağkalım)",
                "Besin yoksunluğunda Atg genleri aktive olur; hasarlı organeller geri dönüştürülerek hücreye enerji ve yapıtaşı sağlanır.",
                "Patolojik Aşırı Rolü (Ölüm)",
                "Stres çözülemezse aşırı otofaji tüm sitoplazmik yapıları tüketir; hücre apoptoz ve nekroz benzeri bir sonla ölür."
            ),
            make_cloze(
                "Açlık ve besin yoksunluğunda hücrenin kendi organellerini sindirerek enerji ürettiği hayatta kalma sürecine otofaji denir.",
                "otofaji",
                "Kendi kendini yeme biyolojik süreci adı"
            )
        ]
    })

    # ADIM 77
    slides.append({
        "slideNumber": 77,
        "title": "Otofajinin Moleküler Evreleri: Atg Genleri ve Otofagozom Mimarisi",
        "subtitle": "Fagofor oluşumu, çift zarlı vezikülün kapatılması ve otofagolizozom füzyonu",
        "badge": "Otofagozom",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Otofaji süreci genetik olarak son derece korunaklı 'Atg' (Autophagy-related genes) proteinleri "
            "tarafından yürütülür. Dört ana basamaktan oluşur:\n\n"
            "1. İndüksiyon ve Fagofor Oluşumu: Besin sensörleri (mTOR inhibisyonu, AMPK aktivasyonu) Atg komplekslerini uyarır. "
            "Sitoplazmada hilal şeklinde bir başlangıç zarı ('Fagofor' / izolasyon membranı) belirir.\n\n"
            "2. Elongasyon ve Otofagozom: Fagofor zarı uzayarak hedeflenen organelleri (mitokondri vb.) çepeçevre sarar "
            "ve kapanır. Ortaya çift zarlı 'Otofagozom' vezikülü çıkar.\n\n"
            "> [SINAV SPOTU] Otofagozom zarına yerleşen 'LC3-II' (Atg8) proteini, laboratuvarda otofajiyi saptamak "
            "için kullanılan evrensel belirteçtir!\n\n"
            "3. Füzyon ve Sindirim: Otofagozom lizozomla kaynaşarak 'Otofagolizozom' olur; asit hidrolazlar içeriği parçalar."
        ),
        "medicalTerms": [
            {"term": "Atg Genleri", "explanation": "Otofajiyi başlatan ve yöneten otofaji ile ilişkili genler ailesi."},
            {"term": "Otofagozom", "explanation": "Sindirilecek organeli saran çift zarlı geçici taşıyıcı vezikül."},
            {"term": "LC3-II", "explanation": "Otofagozom membranına bağlanan ve otofaji aktivitesini gösteren spesifik biyobelirteç."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Otofaji Atg genleri (autophagy-related genes) tarafından yönetilir.",
            "📌 [SINAV SPOTU] Kronolojik sıra: Fagofor -> Çift zarlı Otofagozom -> Otofagolizozom -> Sindirim ve geri dönüşüm.",
            "📌 [SINAV SPOTU] LC3-II otofagozom oluşumunun altın standart moleküler belirtecidir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Atg Orkestrası", "desc": "mTOR kapanması ve AMPK uyarısı ile Atg proteinlerinin toplanması.", "isKey": True},
                {"title": "Otofagolizozom", "desc": "Lizozomal enzimlerin çift zarlı keseyi eritip sindirmesi.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_causal_chain(
                "Otofaji Sürecinin Moleküler Evreleri",
                [
                    "1. Besin Yoksunluğu: Açlık durumunda sitoplazmik sensörler Atg gen ürünlerini aktive eder.",
                    "2. Fagofor Çıkışı: İzolasyon zarı uzayarak sindirilecek organelleri izole etmeye başlar.",
                    "3. Otofagozom Kapanması: Çift zarlı vezikül organeli içine alıp kapanarak otofagozomu oluşturur.",
                    "4. Lizozom Füzyonu: Otofagozom lizozom ile birleşerek otofagolizozom haline gelir.",
                    "5. Sindirim ve Salınım: Lizozom enzimleri organeli parçalar; aminoasit ve glukoz hücreye geri döner."
                ]
            ),
            make_cloze(
                "Otofaji sürecinde organellerin etrafını saran çift zarlı vezikül yapısına otofagozom adı verilir.",
                "otofagozom",
                "Organeli içine alan çift zarlı kesecik adı"
            )
        ]
    })

    # ADIM 78
    slides.append({
        "slideNumber": 78,
        "title": "Otofajinin Klinik ve Hastalık Bağlantıları: Kanser, İnfarkt ve Nörodejenerasyon",
        "subtitle": "İskemik hasar, miyopatiler ve nörodejeneratif hastalıklarda artan otofaji",
        "badge": "Klinik Otofaji",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Ders notumuzda özellikle vurgulandığı üzere, otofaji aktivitesi insan hastalıklarının patogenezinde "
            "iki ucu keskin bir kılıç gibi çalışır. Artmış veya bozulmuş otofaji başlıca 3 büyük klinik alanda izlenir:\n\n"
            "1. İskemik Hasar: Koroner arter tıkanıklığında kardiyomiyositler ATP üretmek için otofajiyi hızlandırır. "
            "Erken evrede koruyucudur ancak kronik iskemide hücreyi tüketebilir.\n\n"
            "2. Nörodejeneratif Hastalıklar: Parkinson, Alzheimer ve ALS'de mutant protein agregatları (Huntingtin, alfa-sinüklein) "
            "normalde otofaji ile temizlenir; otofaji kusurunda bu toksik proteinler nöronları boğarak öldürür.\n\n"
            "> [SINAV SPOTU] Kanser Hücrelerinde Otofaji: Kanser hücreleri tümör merkezindeki damarsız ve aç bölgede "
            "hayatta kalabilmek için otofajiyi aşırı kullanır; kemoterapiye direnç sağlar!\n\n"
            "Ayrıca kas hastalıklarında (miyopatiler) otofajik vakuoller tanısal değere sahiptir."
        ),
        "medicalTerms": [
            {"term": "Agrefaji", "explanation": "Hücre içindeki toksik protein kümelerinin otofaji ile seçici olarak temizlenmesi."},
            {"term": "Mitofaji", "explanation": "Hasarlı ve serbest radikal üreten mitokondrilerin otofajiyle yok edilmesi."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Artmış otofaji: İskemik hasar, miyopatiler ve bazı nörodejeneratif hastalıklarda görülür.",
            "📌 [SINAV SPOTU] Kanser hücreleri kemoterapiye direnç ve açlıkta sağkalım için otofajiyi kullanır.",
            "📌 [SINAV SPOTU] Otofaji bozukluğu nöronlarda toksik protein agregatlarının birikmesine yol açar."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "İskemik Kurtarma", "desc": "Kalp ve beyin infarktında hipoksiye karşı otofajik adaptasyon.", "isKey": True},
                {"title": "Kanser Direnci", "desc": "Tümör kitlelerinin damarsız merkezde otofajiyle beslenmesi.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_branching_logic(
                "İlerlemiş evre pankreas duktal adenokarsinomu olan hastada tümörün derin merkezindeki damarlanması zayıf, hipoksik hücrelerin canlılığını koruduğu görülüyor. Bu tümör hücrelerinin açlıkta hayatta kalma sırrı nedir?",
                [
                    {
                        "text": "Tümör hücreleri fotosentez yaparak kendi besinini üretmektedir.",
                        "isCorrect": False,
                        "feedback": "Biyolojik olarak imkansızdır."
                    },
                    {
                        "text": "Otofaji yolağını (Atg genlerini) aşırı aktive ederek kendi yaşlı organellerini sindirmekte ve açlıkta metabolik yakıt sağlamaktadır.",
                        "isCorrect": True,
                        "feedback": "Kusursuz onkolojik patoloji! Kanser hücreleri besinsiz tümör ortamında otofajiyi sağkalım kalkanı olarak kullanır."
                    },
                    {
                        "text": "Hücreler kazeöz nekroza uğramıştır.",
                        "isCorrect": False,
                        "feedback": "Hatalı! Kazeöz nekroz tüberküloza aittir, tümör canlılığı sağlamaz."
                    }
                ]
            ),
            make_cloze(
                "İskemik hasar, miyopatiler ve nörodejeneratif hastalıklarda hücresel stresi yönetmek için dokuda artmış otofaji izlenir.",
                "otofaji",
                "Hücresel geri dönüşüm mekanizması adı"
            )
        ]
    })

    # ADIM 79 (CHECKPOINT 8)
    slides.append({
        "slideNumber": 79,
        "title": "[TEKRAR SAYFASI - CHECKPOINT 8] Ölüm Biçimleri ve Otofaji Konsolidasyonu",
        "subtitle": "Nekroz vs Apoptoz matrisi, Nekroptoz, Piroptoz, Ferroptoz ve Otofajinin büyük sentezi",
        "badge": "Tekrar Sayfası",
        "badgeColor": "teal",
        "isCheckpoint": True,
        "checkpointNumber": 8,
        "synthesisNarrative": (
            "Bu kontrol noktasında, tıp patolojisinin en modern hücre ölümü haritasını ve alternatif "
            "ölüm biçimlerini eksiksiz konsolide ediyoruz.\n\n"
            "Nekroz ile apoptoz arasındaki kesin çizgiler bellidir: Nekroz = ATP bağımsız, şişme, membran rüptürü, "
            "inflamasyon ve daima patolojik; Apoptoz = ATP bağımlı, büzüşme, membran sağlam, sıfır inflamasyon!\n\n"
            "> [ÖZET REÇETE] Yeni Ölüm Biçimleri Kataloğu:\n"
            "1. Nekroptoz: Kaspaz-bağımsız, RIPK1-RIPK3-MLKL kaskadlı programlı nekroz (TNF uyarılı)\n"
            "2. Piroptoz: İnflamozom, KASPAZ-1, Gazdermin D, IL-1beta salınımı ve YÜKSEK ATEŞ\n"
            "3. Ferroptoz: Demir (Fe²⁺) bağımlı lipid peroksidasyonu, GPX4 iflası\n"
            "4. Otofaji: Atg genleri, Otofagozom (LC3-II), lizozomal sindirim ve hayatta kalma!\n\n"
            "Bu 4'lü modern patoloji sorularının en sıcak konu başlığıdır."
        ),
        "medicalTerms": [
            {"term": "Hücre Ölümü Yelpazesi", "explanation": "Nekroz, apoptoz, nekroptoz, piroptoz ve ferroptozdan oluşan geniş biyolojik yelpaze."},
            {"term": "Nekroptozom vs İnflamozom", "explanation": "Nekroptozda RIPK1/3 kompleksi; piroptozda ise Kaspaz-1'i aktive eden inflamatuar kompleks."}
        ],
        "spotPearls": [
            "📌 [CHECKPOINT ÖZETİ] Nekroz vs Apoptoz: Enerji (yok vs var), Boyut (şişme vs büzüşme), İnflamasyon (var vs yok).",
            "📌 [CHECKPOINT ÖZETİ] Nekroptoz: RIPK1/RIPK3/MLKL ile programlı kaspaz-bağımsız nekroz.",
            "📌 [CHECKPOINT ÖZETİ] Piroptoz: İnflamozom + KASPAZ-1 + IL-1 + Gazdermin D + ATEŞ.",
            "📌 [CHECKPOINT ÖZETİ] Ferroptoz: Demir bağımlı lipid peroksidasyonu ve GPX4 yetmezliği.",
            "📌 [CHECKPOINT ÖZETİ] Otofaji: Atg genleri ve otofagozom ile hayatta kalma mekanizması."
        ],
        "flashcards": [
            make_flashcard(
                "fc-k1-05-22",
                "Kaspaz-bağımsız olan, RIPK1-RIPK3-MLKL sinyal kaskadı ile yürütülen ve morfolojik olarak nekroza benzeyen programlı ölüm biçimi nedir?",
                "Nekroptozdur (Necroptosis)."
            ),
            make_flashcard(
                "fc-k1-05-23",
                "İnflamozom aktivasyonu, Kaspaz-1 devreye girmesi, Gazdermin D delikleri ve IL-1beta salınımı ile yüksek ateşe yol açan hücre ölümü hangisidir?",
                "Piroptozdur (Pyroptosis)."
            ),
            make_flashcard(
                "fc-k1-05-24",
                "Ferroptoz hücre ölümünün temel moleküler mekanizması nedir ve hangi koruyucu enzimin kaybıyla tetiklenir?",
                "Demir (Fe²⁺) bağımlı lipid peroksidasyonudur; Glutatyon Peroksidaz 4 (GPX4) enziminin inaktivasyonuyla tetiklenir."
            )
        ],
        "coreContent": {
            "table": {
                "title": "Modern Hücre Ölümü Biçimleri Büyük Karşılaştırma Tablosu",
                "headers": ["Ölüm Biçimi", "Temel Mekanizma / Moleküller", "Kaspaz Durumu", "İnflamasyon Durumu"],
                "rows": [
                    ["Apoptoz", "Mitokondri (Kaspaz-9) veya Ölüm Reseptörü (Kaspaz-8)", "KASPAZ-BAĞIMLI (3, 8, 9)", "YOK (Sıfır inflamasyon)"],
                    ["Nekroz", "ATP iflası, membran rüptürü, kalsiyum kaosu", "Kaspaz bağımsız", "BELİRGİN ve ŞİDDETLİ"],
                    ["Nekroptoz", "RIPK1, RIPK3, MLKL oligomeri", "KASPAZ-BAĞIMSIZ", "BELİRGİN (Nekroz benzeri)"],
                    ["Piroptoz", "İnflamozom, Gazdermin D, IL-1beta salınımı", "KASPAZ-1 BAĞIMLI", "ÇOK ŞİDDETLİ + YÜKSEK ATEŞ"],
                    ["Ferroptoz", "Demir (Fe²⁺) birikimi, GPX4 kaybı, lipid peroksidasyonu", "Kaspaz bağımsız", "Değişken / Orta derecede"]
                ]
            }
        },
        "interactiveElements": [
            make_table(
                ["Ölüm Tipi", "Ayırt Edici Moleküler İmzası", "Klinik Özelliği"],
                [
                    [("Nekroptoz", False, ""), ("RIPK1 / RIPK3 / MLKL", True, "Kinaz kompleksleri"), ("Kaspaz-8 yokluğunda programlı nekroz", False, "")],
                    [("Piroptoz", False, ""), ("İnflamozom / Kaspaz-1 / Gazdermin D", True, "İnflamatuar kaspaz platformu"), ("IL-1 salınımı ve Yüksek Ateş", False, "")],
                    [("Ferroptoz", False, ""), ("Serbest Fe2+ / GPX4 İnhibisyonu", True, "Demir ve enzim çifti"), ("Demir bağımlı lipid hasarı", False, "")]
                ]
            ),
            make_active_recall(
                "Piroptoz ile klasik apoptoz arasındaki kaspaz tipi ve inflamasyon farkı nedir?",
                "Piroptozda Kaspaz-1 çalışır, yoğun IL-1 salınır ve yüksek ateş/inflamasyon görülür; apoptozda ise Kaspaz-3 çalışır, inflamasyon ve ateş görülmez."
            )
        ]
    })

    # ADIM 80
    slides.append({
        "slideNumber": 80,
        "title": "Hücre Hasarının Biyokimyasal Mekanizmalarına Giriş: Dört Kırılgan Hedef",
        "subtitle": "Mitokondri, hücresel zarlar, DNA ve endoplazmik retikulumun hassas dengesi",
        "badge": "Biyokimya Giriş",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Hücre ölümünün tüm morfolojik kalıplarını (nekroz tipleri, apoptoz ve varyantları) inceledikten sonra, "
            "şimdi bu tabloları doğuran hücresel ve moleküler mekanizmaların derinliklerine iniyoruz.\n\n"
            "Etiyolojik neden ne olursa olsun (toksin, radyasyon, iskemi, enfeksiyon), hasar verici ajanlar "
            "hücrede başlıca 4 kritik hedefe saldırır:\n\n"
            "1. Mitokondri: ATP üretimi çöker, reaktif oksijen türleri (ROS) fırlar.\n"
            "2. Hücresel Zarlar: Plazma, lizozom ve mitokondri zarlarının geçirgenliği bozulur.\n"
            "3. Çekirdek (DNA): Genom kırıkları mutasyon veya apoptozu tetikler.\n"
            "4. Endoplazmik Retikulum: Yanlış katlanmış proteinler birikerek ER stresini başlatır.\n\n"
            "> [SINAV SPOTU] Hücre hasarının nihai sonucu (nekroz mu apoptoz mu) hasarın şiddetine, süresine ve "
            "hücrenin genetik programına bağlı olarak bu 4 sistemin ortak yanıtıyla belirlenir."
        ),
        "medicalTerms": [
            {"term": "Dört Kırılgan Hedef", "explanation": "Hücre hasarında ortak olarak etkilenen mitokondri, membranlar, DNA ve ER yapıları."},
            {"term": "Patobiyokimyasal Kaskad", "explanation": "Bir organdaki hasarın zincirleme olarak diğer organelleri de çökertmesi süreci."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Hücre hasarında başlıca 4 hasar bölgesi vardır: Mitokondri, Hücresel zarlar, Çekirdek (DNA) ve ER.",
            "📌 [SINAV SPOTU] İskemi, radyasyon ve toksinler hem nekroz hem apoptoza yol açabilir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Dört Hedef Organel", "desc": "Mitokondri, membranlar, genom ve protein fabrikası (ER).", "isKey": True},
                {"title": "Yol Ayrımı", "desc": "Şiddetli kriz nekroza, genetik hasar ve hafif stres apoptoza götürür.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Hasar Bölgesi", "Hücresel Sonuç", "Ölüm Yolu Tercihi"],
                [
                    [("Mitokondri", False, ""), ("ATP kaybı ve ROS üretimi", True, "Enerji ve radikal krizi"), ("Ağır hasarda nekroz, sızıntıda apoptoz", False, "")],
                    [("Plazma Zarı", False, ""), ("İyon dengesizliği ve enzim sızıntısı", True, "Membran delinmesi"), ("Doğrudan nekroz", False, "")],
                    [("Çekirdek (DNA)", False, ""), ("p53 aktivasyonu ve genom duraklaması", True, "Genotoksik yanıt"), ("Apoptoz (İçsel yol)", False, "")],
                    [("Endoplazmik Retikulum", False, ""), ("Katlanmamış protein birikimi (ER stresi)", True, "Şaperon yetmezliği"), ("Apoptoz (UPR terminal)", False, "")]
                ]
            ),
            make_cloze(
                "Hücre hasarında hasar verici etkenlerin en savunmasız bulduğu başlıca 4 hedef mitokondri, hücresel zarlar, DNA ve endoplazmik retikulumdur.",
                "mitokondri",
                "ATP fabrikası olan hücre hasarının birinci organel hedefi"
            )
        ]
    })

    return slides
