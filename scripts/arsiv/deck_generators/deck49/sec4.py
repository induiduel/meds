import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from meds.scripts.deck_generators.builder_helper import make_slide, make_cloze, make_table, make_chain, make_recall, make_spot_lie, make_quiz

def get_sec4():
    slides = []

    # Slide 31: Viral Genom Entegrasyonu: Episomal vs Entegre DNA
    s31_narrative = (
        "Human Papilloma Virus genomunun hücre içindeki fiziksel durumu, lezyonun selim bir siğil mi "
        "yoksa malign bir karsinom mu olacağını belirleyen en kritik moleküler dönemeçtir.\n\n"
        "- **Episomal Form (Düşük Risk):** HPV 6 ve 11 gibi düşük riskli tiplerde viral DNA konak kromozomlarına "
        "katılmaz; çekirdekte bağımsız, dairesel **episomal plazmit benzeri formda** kalır.\n"
        "- **Konak Genomuna Entegrasyon (Yüksek Risk):** HPV 16 ve 18 gibi yüksek riskli tipler, persistan enfeksiyon "
        "sırasında viral DNA'larını **insan kromozomlarına entegre ederler**.\n"
        "- **Karsinojenik Kırılma:** Entegrasyon rastgele bir olay olmayıp invaziv karsinom gelişimine giden "
        "biyolojik dönüşümün en önemli moleküler basamağıdır.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Düşük riskli HPV tiplerinde DNA episomal kalırken; yüksek riskli tipler konak genomuna entegre olarak karsinogenezi tetikler."
    )
    s31_bullets = [
        "Düşük riskli tiplerde viral DNA bağımsız episomal formda kalır.",
        "Yüksek riskli tipler (16, 18) konak kromozomlarına entegre olur.",
        "Genomik entegrasyon karsinogeneze ilerlemenin kilit basamağıdır."
    ]
    s31_elements = [
        make_cloze("Düşük riskli HPV tiplerinde viral DNA konak kromozomuna girmeyip episomal olarak çekirdekte kalır.", "episomal", "Bağımsız dairesel plazmit benzeri varoluş biçimi"),
        make_table("Viral Genom Durumu Karşılaştırması", ["HPV Tipi", "Genom Fiziksel Durumu", "Klinik Seyir"], [
            {"cells": [{"text": "Düşük Risk (HPV 6, 11)", "isMasked": False}, {"text": "Episomal dairesel form", "isMasked": True, "hint": "kromozom dışı bağımsız varlık"}, {"text": "Benign siğil (kondilom)"}]},
            {"cells": [{"text": "Yüksek Risk (HPV 16, 18)", "isMasked": False}, {"text": "Konak genomuna entegre form", "isMasked": False}, {"text": "Genomik instabilite ve karsinom", "isMasked": True, "hint": "malign neoplazi süreci"}]}
        ]),
        make_chain("Viral Genom Entegrasyonu Basamakları", [
            "1. Persistan Varlık: Yüksek riskli HPV uzun süre servikal bazal hücrede çoğalır.",
            "2. Genomik Kırılma: Viral halka şeklindeki DNA'da ve konak kromozomunda çift zincir kırıkları oluşur.",
            "3. Entegrasyon: Viral DNA insan kromozomunun içine kalıcı olarak monte edilir.",
            "4. Malign Transformasyon: Kontrol mekanizmaları koparak onkoprotein fırtınası başlar."
        ]),
        make_recall("Düşük riskli HPV tipleri ile yüksek riskli tipler arasındaki temel genomik fiziksel fark nedir?", "Düşük risklilerde DNA konak kromozomuna girmeyip episomal kalırken; yüksek risklilerde konak genomuna entegre olur."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Viral Genom Entegrasyonu", [
            {"text": "Düşük riskli tiplerde DNA konak genomuna entegre olmaz, episomal kalır.", "isLie": False, "explanation": "Doğru. HPV 6 ve 11 episomaldir."},
            {"text": "Yüksek riskli tiplerin entegrasyonu malign progresyon ile ilişkilidir.", "isLie": False, "explanation": "Doğru. Entegrasyon karsinogenezin basamağıdır."},
            {"text": "Viral entegrasyon gerçekleştiğinde konak hücresi hemen bakteri hücresine dönüşür.", "isLie": True, "explanation": "Tuzak! Konak hücresi bakteri olmaz; insan ökaryotik hücresidir, viral genleri taşımaya başlar."},
            {"text": "HPV 16 ve 18 konak kromozomuna entegre olma eğilimindedir.", "isLie": False, "explanation": "Doğru. Entegrasyon yüksek risklilerin özelliğidir."}
        ]),
        make_quiz("Düşük riskli HPV tipleri (6 ve 11) ile ilgili genomik özellik aşağıdakilerden hangisidir?", [
            {"key": "A", "text": "Viral DNA konak genomuna entegre olmaz, episomal kalır", "isCorrect": True, "explanation": "Düşük riskli tipler episomal kalır ve entegre olmaz."},
            {"key": "B", "text": "Hemen insan kromozomunun tümünü parçalayıp yok eder", "isCorrect": False, "explanation": "Kromozomları yok etmez."},
            {"key": "C", "text": "Zorunlu olarak daima invaziv kanser üretir", "isCorrect": False, "explanation": "Benign siğil yapar, kanser yapmaz."},
            {"key": "D", "text": "DNA içermez, sırf lipit damlacığından ibarettir", "isCorrect": False, "explanation": "DNA virüsüdür."}
        ])
    ]
    slides.append(make_slide(31, "Viral Genom Entegrasyonu: Episomal vs Entegre DNA", "Fiziksel genom formu, konak kromozomuna katılma, episomal kararlılık", "Moleküler Genetik: Entegrasyon", s31_narrative, s31_bullets, s31_elements))

    # Slide 32: E2 Geninin Bozulması ve Onkoprotein Aşırı Salımı
    s32_narrative = (
        "Yüksek riskli HPV genomu insan DNA'sına entegre olurken rastgele bir noktadan değil, "
        "virüsün kendi iç dengesini sağlayan özel bir genden kırılarak açılır.\n\n"
        "- **E2 Gen Kırılması:** Entegrasyon sırasında viral DNA'nın dairesel halkası **E2 repressör geni bölgesinden kırılır** "
        "ve bu genin bütünlüğü tamamen parçalanır.\n"
        "- **E2'nin Normal Görevi:** Normalde intact E2 proteini, viral erken promotörü baskılayarak "
        "E6 ve E7 onkoproteinlerinin aşırı düzeyde üretilmesini engelleyen bir **negatif fren mekanizmasıdır**.\n"
        "- **Onkogen Fırtınası:** E2 geni bozulunca fren mekanizması ortadan kalkar; hücre içinde kontrolsüz ve "
        "devasa miktarda **E6 ve E7 onkoproteini eksprese edilmeye başlar**.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Viral DNA entegrasyonu E2 genini bozar; E2 baskısı ortadan kalkınca E6 ve E7 ekspresyonu kontrolsüz biçimde katlanarak artar."
    )
    s32_bullets = [
        "Entegrasyon sırasında viral E2 repressör geni parçalanır.",
        "Normalde E2, E6 ve E7 onkoproteinlerini negatif regüle eder.",
        "E2 inaktivasyonu aşırı E6 ve E7 ekspresyonuna yol açar."
    ]
    s32_elements = [
        make_cloze("Viral entegrasyon E6 ve E7 üretimini frenleyen E2 gen bölgesinin parçalanmasına yol açar.", "E2", "Viral onkoproteinleri negatif düzenleyen gen"),
        make_table("E2 Geninin Fonksiyonel Durumu", ["Durum", "E2 Gen Bütünlüğü", "E6 ve E7 Üretim Düzeyi"], [
            {"cells": [{"text": "Episomal Faz", "isMasked": False}, {"text": "İntact ve fonksiyonel E2 geni", "isMasked": True, "hint": "bozulmamış gen yapısı"}, {"text": "Kontrollü ve düşük düzeyde sentez"}]},
            {"cells": [{"text": "Entegre Faz", "isMasked": False}, {"text": "Parçalanmış ve inaktif E2 geni", "isMasked": False}, {"text": "Frensiz, aşırı ve kontrolsüz salım", "isMasked": True, "hint": "baskılanamayan devasa transkripsiyon"}]}
        ]),
        make_chain("E2 Bozulmasından Karsinogeneze", [
            "1. Genomik Entegrasyon: Virüs insan DNA'sına E2 lokusundan kırılarak bağlanır.",
            "2. E2 İnaktivasyonu: Negatif düzenleyici E2 transkripsiyon faktörü üretilemez.",
            "3. Promotör Aktivasyonu: Erken viral promotör sürekli açık kalarak E6/E7 genlerini okur.",
            "4. Hücresel Yıkım: Aşırı E6 ve E7 p53 ile RB'yi tüketerek malign transformasyonu tamamlar."
        ]),
        make_recall("Yüksek riskli HPV entegrasyonu sırasında hangi viral genin bozulması E6 ve E7 onkoproteinlerinin aşırı salımına yol açar?", "Viral negatif düzenleyici E2 geni bozulur."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: E2 Geni ve Onkoprotein Salımı", [
            {"text": "Viral entegrasyon E6 ve E7'yi negatif düzenleyen E2 genini bozar.", "isLie": False, "explanation": "Doğru. Kırılma E2 bölgesinde gerçekleşir."},
            {"text": "E2 geni bozulunca E6 ve E7 ekspresyonu belirgin şekilde artar.", "isLie": False, "explanation": "Doğru. Negatif fren ortadan kalkar."},
            {"text": "E2 geni bozulduğu anda tüm viral proteinler yok olup hasta mucizevi şekilde iyileşir.", "isLie": True, "explanation": "Tuzak! Tam aksine E2 bozulunca virüsün karsinojenik E6 ve E7 proteinleri patlama yapar ve kanserleşme hızlanır."},
            {"text": "E2 normalde onkoprotein ekspresyonunu frenleyen bir viral gendir.", "isLie": False, "explanation": "Doğru. Normal görevi kontrolü sağlamaktır."}
        ]),
        make_quiz("HPV genomunun insan DNA'sına entegrasyonu sırasında E2 geninin bozulmasının biyolojik sonucu nedir?", [
            {"key": "A", "text": "E6 ve E7 onkoprotein ekspresyonunun aşırı derecede artması", "isCorrect": True, "explanation": "E2 freni kalkınca E6 ve E7 üretimi kontrolsüzce artar."},
            {"key": "B", "text": "Virüsün anında parçalanarak yok olması", "isCorrect": False, "explanation": "Virüs yok olmaz, karsinogenez ilerler."},
            {"key": "C", "text": "Hücrenin insülin üretmeye başlaması", "isCorrect": False, "explanation": "Hormon senteziyle ilgisi yoktur."},
            {"key": "D", "text": "Kromozomların kemik matriksine dönüşmesi", "isCorrect": False, "explanation": "Kemikleşme görülmez."}
        ])
    ]
    slides.append(make_slide(32, "E2 Geninin Bozulması ve Onkoprotein Aşırı Salımı", "E2 kırılması, negatif regülasyon kaybı, E6/E7 ekspresyon patlaması", "Regülasyon Mekanizması: E2", s32_narrative, s32_bullets, s32_elements))

    # Slide 33: SIL ve CIN Terminolojisi: Sitoloji vs Histoloji
    s33_narrative = (
        "Servikal kanser öncüsü lezyonların tanımlanmasında laboratuvar disiplinlerine göre iki temel "
        "terminoloji sistemi paralel olarak kullanılır.\n\n"
        "- **SIL (Skuamöz İntraepitelyal Lezyon):** Temelde **sitolojik** incelemelerde (Pap smear) ve klinik "
        "yönetim kılavuzlarında kullanılan iki basamaklı (LSIL ve HSIL) Bethesda sınıflamasıdır.\n"
        "- **CIN (Servikal İntraepitelyal Neoplazi):** Doku biyopsilerinde uygulanan **histopatolojik** sınıflamadır; "
        "displastik hücrelerin epitel kalınlığı boyunca yayılımına göre üç basamakta (CIN I, CIN II, CIN III) incelenir.\n"
        "- **Klinik Karşılık:** LSIL histopatolojik olarak CIN I ile örtüşürken; HSIL grubu hem CIN II hem de CIN III lezyonlarını kapsar.\n\n"
        "> [!NOTE]\n"
        "> SIL sitolojik (Pap smear) iki basamaklı sınıflamayken; CIN biyopsideki üç basamaklı histolojik sınıflamadır."
    )
    s33_bullets = [
        "SIL sitolojide (Pap smear), CIN histolojide (biyopsi) kullanılır.",
        "SIL iki basamaklıdır: LSIL (düşük dereceli) ve HSIL (yüksek dereceli).",
        "CIN üç basamaklıdır: CIN I, CIN II ve CIN III (karsinoma in situ)."
    ]
    s33_elements = [
        make_cloze("Doku biyopsilerinde epitel içi displaziyi üç basamakta inceleyen histopatolojik sınıflama CIN olarak adlandırılır.", "CIN", "Servikal intraepitelyal neoplazi kısaltması"),
        make_table("Terminoloji Karşılaştırması: Sitoloji vs Histoloji", ["Klinik/Sitolojik Terim (SIL)", "Histopatolojik Karşılığı (CIN)", "Biyolojik Anlamı"], [
            {"cells": [{"text": "LSIL (Düşük Dereceli SIL)", "isMasked": False}, {"text": "CIN I (Hafif Displazi)", "isMasked": True, "hint": "alt üçte bir tutulumu"}, {"text": "Viral replikasyon ve koilositoz"}]},
            {"cells": [{"text": "HSIL (Yüksek Dereceli SIL)", "isMasked": False}, {"text": "CIN II ve CIN III", "isMasked": False}, {"text": "Gerçek karsinom öncülü neoplazi", "isMasked": True, "hint": "maligniteye ilerleyebilen lezyon"}]}
        ]),
        make_chain("Sitolojiden Histolojik Tanıya", [
            "1. Tarama Smeari: Eksfoliye hücrelerde nükleer büyüme ve koilositoz görülür (SIL).",
            "2. Kolposkopi: Şüpheli asetobeyaz epitel alanından forseps ile doku biyopsisi alınır.",
            "3. Histopatolojik Kesit: Doku katmanları, tabakalaşma ve mitoz derinliği taranır (CIN).",
            "4. Yönetim Kararı: CIN derecesine göre konservatif takip veya cerrahi eksizyon planlanır."
        ]),
        make_recall("Serviks kanser öncüllerinde sitolojik sınıflama ile histopatolojik sınıflama arasındaki fark nedir?", "Sitolojik sınıflama iki basamaklı SIL (LSIL/HSIL); histopatolojik sınıflama ise üç basamaklı CIN'dir (CIN I, II, III)."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: SIL ve CIN Terminolojisi", [
            {"text": "SIL sitolojide, CIN ise histopatolojik biyopsi değerlendirmesinde kullanılır.", "isLie": False, "explanation": "Doğru. Disiplin bazlı terminoloji ayrımıdır."},
            {"text": "LSIL histolojide CIN I'e, HSIL ise CIN II ve CIN III'e karşılık gelir.", "isLie": False, "explanation": "Doğru. Bethesda ile histoloji paralelliğidir."},
            {"text": "CIN terimi yalnızca erkeklerde prostat bezinde gelişen kistleri ifade eder.", "isLie": True, "explanation": "Tuzak! CIN kadınlarda servikal intraepitelyal neoplaziyi tanımlar; prostatla hiçbir ilgisi yoktur."},
            {"text": "CIN sınıflaması displazinin epitel kalınlığındaki derinliğine göre yapılır.", "isLie": False, "explanation": "Doğru. Alt 1/3, 2/3 ve tam kalınlık ayrımıdır."}
        ]),
        make_quiz("Servikal intraepitelyal neoplazi (CIN) sınıflaması temel olarak hangi tanı materyalinde uygulanır?", [
            {"key": "A", "text": "Doku biyopsisi kesitlerinde histopatolojik incelemede", "isCorrect": True, "explanation": "CIN histopatolojik biyopsi sınıflamasıdır."},
            {"key": "B", "text": "Yalnızca periferik kan yaymasında lökosit sayımında", "isCorrect": False, "explanation": "Kanda CIN bakılmaz."},
            {"key": "C", "text": "Röntgen filminde kemik yoğunluğu ölçümünde", "isCorrect": False, "explanation": "Radyolojik kemik ölçümü değildir."},
            {"key": "D", "text": "Sadece idrar tahlilinde şeker aramasında", "isCorrect": False, "explanation": "İdrar biyokimyası değildir."}
        ])
    ]
    slides.append(make_slide(33, "SIL ve CIN Terminolojisi: Sitoloji vs Histoloji", "Bethesda sistemi, LSIL/HSIL, CIN I/II/III, klinik ve patolojik eşleşme", "Terminoloji ve Sınıflama", s33_narrative, s33_bullets, s33_elements))

    # Slide 34: LSIL (CIN I): Tanım, Histoloji ve Alt 1/3 Tutulumu
    s34_narrative = (
        "LSIL (Düşük Dereceli Skuamöz İntraepitelyal Lezyon), histopatolojide **CIN I (hafif displazi)** olarak adlandırılan "
        "ve HPV enfeksiyonunun morfolojik yansımasını gösteren tablodur.\n\n"
        "- **Tutulum Derinliği:** Displastik ve hiperkromatik atipik hücreler skuamöz epitelin yalnızca "
        "**alt üçte birine (1/3)** sınırlıdır; üstteki 2/3'lük epitel katmanında olgunlaşma korunmuştur.\n"
        "- **Viral Aktivite:** Bu evrede viral replikasyon son derece aktiftir; epitel içinde virion üretimi yüksektir "
        "ancak konak hücre kontrolü henüz tam olarak kaybedilmemiştir.\n"
        "- **Biyolojik Anlam:** LSIL gerçek anlamda bir kanser öncülü sayılmaz; yüksek oranda geçici bir viral enfeksiyon tezahürüdür.\n\n"
        "> [!NOTE]\n"
        "> LSIL (CIN I) olgularında nükleer atipi ve displazi epitelin sadece alt 1/3 tabakasına sınırlıdır."
    )
    s34_bullets = [
        "Displazi epitelin yalnızca alt üçte birine sınırlıdır.",
        "Epitelin üst 2/3 tabakasında olgunlaşma devam eder.",
        "Viral replikasyon yüksek olup geçici enfeksiyon tablosudur."
    ]
    s34_elements = [
        make_cloze("LSIL (CIN I) lezyonunda hücresel displazi epitelin alt üçte bir tabakasına sınırlı kalır.", "üçte bir", "Tutulan epitel derinliği fraksiyonu"),
        make_table("LSIL (CIN I) Histopatolojik Özellikleri", ["Katman", "Hücresel Morfoloji", "Patolojik Özellik"], [
            {"cells": [{"text": "Epitel Alt 1/3", "isMasked": False}, {"text": "Displastik bazal benzeri atipik hücreler", "isMasked": True, "hint": "derin katman hücresel atipisi"}, {"text": "Hafif nükleer pleomorfizm ve mitoz"}]},
            {"cells": [{"text": "Epitel Üst 2/3", "isMasked": False}, {"text": "Farklılaşmış, yassılaşmış hücreler", "isMasked": False}, {"text": "Olgunlaşma korunur, koilositler eşlik eder", "isMasked": True, "hint": "yüzeyel diferansiyasyon devamı"}]}
        ]),
        make_chain("CIN I Doku Mimarisi", [
            "1. Bazal Tutulum: Atipik hücreler bazal membranın hemen üzerinde çoğalır.",
            "2. Sınır: Atipi epitel kalınlığının alt 1/3 seviyesini kesinlikle aşmaz.",
            "3. Diferansiyasyon: Hücreler yukarı göç ederken sitoplazmaları genişler ve yassılaşır.",
            "4. Yüzeyel Dökülme: Yüzeyden canlı virüs parçacıkları vajinal ortama dökülür."
        ]),
        make_recall("CIN I lezyonunda displastik hücrelerin epitel kalınlığı içindeki yayılım sınırı nedir?", "Displazi epitel kalınlığının alt 1/3'lük kısmına sınırlıdır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: LSIL (CIN I) Histolojisi", [
            {"text": "CIN I'de displazi epitelin alt üçte birindedir.", "isLie": False, "explanation": "Doğru. Alt 1/3 derinlikle sınırlıdır."},
            {"text": "Viral replikasyon bu lezyonlarda oldukça aktiftir.", "isLie": False, "explanation": "Doğru. Virion üretimi yüksektir."},
            {"text": "CIN I'de atipik hücreler tüm epitel kalınlığını kaplayıp kemik iliğine invazyon yapmıştır.", "isLie": True, "explanation": "Tuzak! CIN I sadece alt 1/3'e sınırlıdır; invazyon yapmaz, karsinom değildir."},
            {"text": "Epitelin üst katmanlarında olgunlaşma korunur.", "isLie": False, "explanation": "Doğru. Diferansiyasyon devam eder."}
        ]),
        make_quiz("LSIL (CIN I) lezyonunun histopatolojik tanısında displazinin epitel içindeki derinliği nasıldır?", [
            {"key": "A", "text": "Displazi skuamöz epitelin alt üçte birinde sınırlıdır", "isCorrect": True, "explanation": "CIN I'de atipik hücreler epitelin alt 1/3'ündedir."},
            {"key": "B", "text": "Epitelin tam kalınlığını kaplayan anaplastik tümördür", "isCorrect": False, "explanation": "Bu CIN III / CIS tanımıdır."},
            {"key": "C", "text": "Sadece çizgili kas hücrelerinde görülen bir hasardır", "isCorrect": False, "explanation": "Skuamöz epitel lezyonudur."},
            {"key": "D", "text": "Bazal membranı tamamen parçalayıp rektuma yayılmıştır", "isCorrect": False, "explanation": "İnvaziv değildir, intraepitelyaldir."}
        ])
    ]
    slides.append(make_slide(34, "LSIL (CIN I): Tanım, Histoloji ve Alt 1/3 Tutulumu", "Alt 1/3 tutulumu, epitel diferansiyasyonu, viral replikasyon ve hafif displazi", "Preinvaziv Histopatoloji: CIN I", s34_narrative, s34_bullets, s34_elements))

    # Slide 35: Koilositik Değişiklik: HPV'nin Sitopatik Etkisi
    s35_narrative = (
        "HPV enfeksiyonunun ışık mikroskobundaki en karakteristik patognomonik morfolojik kanıtı "
        "**koilositik değişiklik (koilositoz)** olarak adlandırılan hücresel hasardır.\n\n"
        "- **Koilosit Morfolojisi:** Koilositler, düzensiz sınırlı (kuru üzüm benzeri), hiperkromatik nükleus etrafında "
        "geniş ve keskin sınırlı **şeffaf perinükleer halo (boşluk)** içeren özelleşmiş skuamöz hücrelerdir.\n"
        "- **Lokalizasyon:** Koilositik değişiklikler tipik olarak epitelin **yüzeysel ve orta katmanlarındaki** "
        "diferansiye hücrelerde belirgindir; çünkü viral L1 ve L2 kapsid proteinleri bu katmanlarda monte edilir.\n"
        "- **Diagnostik Rol:** Hem Pap smear sitolojisinde hem de biyopside koilosit görülmesi aktif HPV varlığının kesin kanıtıdır.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Koilositik değişiklik (hiperkromatik nükleus + perinükleer şeffaf halo), HPV enfeksiyonunun karakteristik mikroskobik sitopatik etkisidir ve LSIL'de epitelin üst katmanlarında izlenir."
    )
    s35_bullets = [
        "Koilositoz, HPV'nin karakteristik sitopatik etkisidir.",
        "Hiperkromatik nükleus etrafında şeffaf perinükleer halo ile karakterizedir.",
        "Epitelin yüzeysel ve orta katmanlarında en belirgin şekilde izlenir."
    ]
    s35_elements = [
        make_cloze("Hiperkromatik nükleus etrafında geniş şeffaf halo içeren HPV sitopatik hücresine koilosit adı verilir.", "koilosit", "HPV enfeksiyonunun karakteristik halo gösteren hücresi"),
        make_table("Koilosit Morfolojisinin Temel Bileşenleri", ["Hücresel Alan", "Mikroskobik Morfoloji", "Biyolojik Nedeni"], [
            {"cells": [{"text": "Hücre Çekirdeği", "isMasked": False}, {"text": "Hiperkromatik, buruşuk, büyük nükleus", "isMasked": True, "hint": "koyu boyanan atipik çekirdek"}, {"text": "Viral DNA replikasyonu ve nükleer hasar"}]},
            {"cells": [{"text": "Sitoplazma", "isMasked": False}, {"text": "Geniş berrak perinükleer halo", "isMasked": False}, {"text": "Viral E5/E4 etkisiyle sitoskeleton çöküşü", "isMasked": True, "hint": "hücre iskeleti vakuolizasyonu"}]}
        ]),
        make_chain("Koilosit Oluşum Mekanizması", [
            "1. Viral Montaj: Epitelin üst katmanlarında virüs kapsid proteinlerini üretir.",
            "2. Sitoskeletal Hasar: Sitokeratin filamentleri nükleus çevresinden perifere itilir.",
            "3. Halo Belirmesi: Çekirdek çevresinde optik olarak boş, şeffaf bir zon oluşur.",
            "4. Eksfoliasyon: Koilositik hücre servikal yüzeyden dökülerek Pap smear'de yakalanır."
        ]),
        make_recall("HPV'nin mikroskopta tanınmasını sağlayan karakteristik hücresel bulgusu nedir ve nasıl görünür?", "Koilositik değişikliktir; buruşuk hiperkromatik nükleus etrafında berrak perinükleer halo şeklinde izlenir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Koilositik Değişiklik", [
            {"text": "Koilosit çekirdek etrafında geniş perinükleer halo ile karakterizedir.", "isLie": False, "explanation": "Doğru. Tipik şeffaf hale görünümüdür."},
            {"text": "Koilositik değişiklik HPV enfeksiyonunun mikroskobik sitopatik bulgusudur.", "isLie": False, "explanation": "Doğru. HPV varlığının doğrudan kanıtıdır."},
            {"text": "Koilositler kemik iliğindeki trombosit üreten megakaryosit hücreleridir.", "isLie": True, "explanation": "Tuzak! Koilosit servikal skuamöz epitel hücresidir; kemik iliği veya megakaryosit ile ilgisi yoktur."},
            {"text": "LSIL lezyonlarında yüzeysel epitel katmanlarında sıkça görülür.", "isLie": False, "explanation": "Doğru. Yüzeyel katmanlarda belirgindir."}
        ]),
        make_quiz("HPV enfeksiyonunu gösteren patognomonik koilosit hücresinin tipik mikroskobik görünümü nasıldır?", [
            {"key": "A", "text": "Buruşuk hiperkromatik nükleus etrafında belirgin şeffaf perinükleer halo", "isCorrect": True, "explanation": "Koilositin kardinal özelliği hiperkromatik çekirdek ve perinükleer halodur."},
            {"key": "B", "text": "Kırmızı kan hücreleri ile dolup taşmış fagositik lökosit", "isCorrect": False, "explanation": "Eritrofagositoz yapan makrofaj değildir."},
            {"key": "C", "text": "Çekirdeği olmayan bikonkav disk şeklinde eritrosit", "isCorrect": False, "explanation": "Kırmızı kan hücresi değildir."},
            {"key": "D", "text": "Çok çekirdekli osteoklast benzeri dev kemik hücresi", "isCorrect": False, "explanation": "Osteoklast değildir."}
        ])
    ]
    slides.append(make_slide(35, "Koilositik Değişiklik: HPV'nin Sitopatik Etkisi", "Perinükleer halo, nükleer hiperkromazi, sitopatik etki ve tanısal önemi", "Sitopatoloji: Koilositoz", s35_narrative, s35_bullets, s35_elements))

    # Slide 36: LSIL Neden Prekanseröz Kabul Edilmez? Doğal Seyir
    s36_narrative = (
        "Patoloji ve jinekolojik onkoloji pratiğinde LSIL (CIN I), yaygın kanının aksine doğrudan bir "
        "kanser öncülü (prekanseröz) olarak kabul edilmez.\n\n"
        "- **Yüksek Spontan Regresyon Oranı:** LSIL tanısı alan olguların **yaklaşık %60'ı hiçbir tedaviye "
        "gerek kalmaksızın spontan olarak kendiliğinden geriler** ve tamamen normale döner.\n"
        "- **Persistans ve İlerleme:** Olguların yaklaşık **%30'u sebat eder (persiste kalır)**; yalnızca "
        "küçük bir bölümü olan **%10'u HSIL'e ilerler**.\n"
        "- **Biyolojik Nitelik:** Bu tablo kontrolsüz bir neoplaziden ziyade, immün sistemin henüz temizlemekte "
        "olduğu geçici, üretken bir viral enfeksiyonu temsil eder.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] LSIL (CIN I) prekanseröz kabul edilmez; çünkü vakaların %60'ı spontan geriler, %30'u sebat eder, sadece %10'u HSIL'e ilerler."
    )
    s36_bullets = [
        "LSIL vakalarının yaklaşık %60'ı kendiliğinden geriler.",
        "Yaklaşık %30'u persiste kalır, yalnızca %10'u HSIL'e ilerler.",
        "Bu yüksek regresyon oranı nedeniyle lezyon prekanseröz kabul edilmez."
    ]
    s36_elements = [
        make_cloze("LSIL olgularının yaklaşık yüzde 60 oranı spontan olarak tamamen gerilediğinden prekanseröz kabul edilmez.", "yüzde 60", "Kendiliğinden gerileyen LSIL oranı"),
        make_table("LSIL (CIN I) Doğal Seyir İstatistikleri", ["Klinik Akıbet", "Görülme Yüzdesi", "Klinik Yönetim Anlamı"], [
            {"cells": [{"text": "Spontan Regresyon (Gerileme)", "isMasked": False}, {"text": "%60", "isMasked": True, "hint": "olguların yarıdan fazlası"}, {"text": "Agresif cerrahiden kaçınma gerekçesi"}]},
            {"cells": [{"text": "Persistans (Sebat Etme)", "isMasked": False}, {"text": "%30", "isMasked": False}, {"text": "Aralıklı sitolojik takip gerekliliği", "isMasked": True, "hint": "düzenli izlem gereği"}]},
            {"cells": [{"text": "HSIL'e Progresyon (İlerleme)", "isMasked": False}, {"text": "%10", "isMasked": True, "hint": "en küçük hasta grubu"}, {"text": "İlerleyen azınlıkta eksizyon"}]}
        ]),
        make_chain("LSIL Klinik Akıbet Dağılımı", [
            "1. LSIL Tanısı: Biyopsi veya sitolojide CIN I saptanır.",
            "2. İmmün Yanıt: Konağın T hücreleri enfekte hücrelere karşı aktive olur.",
            "3. %60 Çözülme: Çoğu kadında 1-2 yıl içinde lezyon tamamen kaybolur.",
            "4. Konservatif İzlem: Hastaya gereksiz cerrahi yapılmayıp periyodik takiple izlenir."
        ]),
        make_recall("LSIL'in (CIN I) prekanseröz bir lezyon olarak kabul edilmemesinin temel gerekçesi nedir?", "Olguların %60 gibi büyük bir kısmının spontan olarak kendiliğinden gerilemesi ve sadece %10'unun HSIL'e ilerlemesidir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: LSIL Doğal Seyri", [
            {"text": "LSIL vakalarının yaklaşık %60'ı kendiliğinden geriler.", "isLie": False, "explanation": "Doğru. Regresyon oranı %60'tır."},
            {"text": "LSIL vakalarının yalnızca %10'u HSIL'e ilerler.", "isLie": False, "explanation": "Doğru. İlerleme oranı düşüktür."},
            {"text": "LSIL tanısı konan tüm kadınlarda 1 ay içinde istisnasız invaziv karsinom gelişir.", "isLie": True, "explanation": "Tuzak! LSIL'in %60'ı kendiliğinden geçer; doğrudan kansere gitmez, prekanseröz bile sayılmaz."},
            {"text": "LSIL genellikle geçici üretken viral enfeksiyonu yansıtır.", "isLie": False, "explanation": "Doğru. Kendini sınırlayan viral tablodur."}
        ]),
        make_quiz("LSIL (CIN I) lezyonunun doğal seyrindeki spontan regresyon (kendiliğinden gerileme) oranı kaçtır?", [
            {"key": "A", "text": "%60", "isCorrect": True, "explanation": "LSIL'in yaklaşık %60'ı spontan geriler."},
            {"key": "B", "text": "%0 (Hiçbir zaman gerilemez)", "isCorrect": False, "explanation": "Büyük çoğunluğu geriler."},
            {"key": "C", "text": "%100 (İstisnasız hepsi 2 günde biter)", "isCorrect": False, "explanation": "Bir kısmı sebat eder veya ilerler."},
            {"key": "D", "text": "%1", "isCorrect": False, "explanation": "Gerileme oranı çok daha yüksektir (%60)."}
        ])
    ]
    slides.append(make_slide(36, "LSIL Neden Prekanseröz Kabul Edilmez? Doğal Seyir", "Spontan regresyon (%60), persistans (%30), progresyon (%10) ve biyolojik anlam", "Doğal Seyir ve Regresyon", s36_narrative, s36_bullets, s36_elements))

    # Slide 37: HSIL (CIN II ve CIN III): Tanım ve Tutulum Derinliği
    s37_narrative = (
        "HSIL (Yüksek Dereceli Skuamöz İntraepitelyal Lezyon), histopatolojide **CIN II ve CIN III** "
        "kategorilerini kapsayan, gerçek anlamda prekanseröz kabul edilen neoplazik süreçtir.\n\n"
        "- **CIN II (Orta Dereceli Displazi):** Atipik, bazal benzeri immatür hücreler epitel kalınlığının "
        "**alt üçte ikisini (2/3)** tutmuştur; üst 1/3'te kısmi olgunlaşma izlenebilir.\n"
        "- **CIN III (Ağır Displazi / Karsinoma in Situ):** Atipik hücreler skuamöz epitelin **tam kalınlığını (tüm katlarını)** "
        "tutmuştur; hücresel polarite ve epitel olgunlaşması tamamen kaybolmuştur.\n"
        "- **Biyolojik Davranış:** Viral replikasyon durmuş veya çok azalmıştır; hücresel proliferasyon frensiz hale gelmiştir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] HSIL spektrumunda CIN II epitelin alt 2/3'ünü tutarken; CIN III epitelin tam kalınlığını (tam kat) tutar ve olgunlaşma tamamen kaybolmuştur."
    )
    s37_bullets = [
        "HSIL gerçek prekanseröz lezyondur; CIN II ve CIN III'ü kapsar.",
        "CIN II epitelin alt 2/3'ünü, CIN III tam kalınlığını tutar.",
        "Epitel polaritesi bozulmuş, matürasyon tamamen durmuştur."
    ]
    s37_elements = [
        make_cloze("HSIL spektrumunda atipik hücrelerin epitelin tam kalınlığını kapladığı lezyon CIN III olarak tanımlanır.", "CIN III", "Ağır displazi ve karsinoma in situ evresi"),
        make_table("CIN Evrelerine Göre Epitel Tutulum Derinliği", ["Histolojik Evre", "Tutulan Epitel Derinliği", "Diferansiyasyon / Olgunlaşma"], [
            {"cells": [{"text": "CIN I (LSIL)", "isMasked": False}, {"text": "Alt 1/3 tabaka", "isMasked": False}, {"text": "Üst katmanlarda iyi olgunlaşma korunur"}]},
            {"cells": [{"text": "CIN II (HSIL)", "isMasked": False}, {"text": "Alt 2/3 tabaka", "isMasked": True, "hint": "epitelin üçte ikisi"}, {"text": "Yalnızca en üst tabakada hafif olgunlaşma"}]},
            {"cells": [{"text": "CIN III (HSIL)", "isMasked": False}, {"text": "Tam kalınlık (tüm katmanlar)", "isMasked": True, "hint": "bütün epitel katları"}, {"text": "Olgunlaşma tamamen durmuştur", "isMasked": False}]}
        ]),
        make_chain("CIN Progresyon Basamakları", [
            "1. CIN I: Displazi alt 1/3'te sınırlıdır, yüzeyde koilositoz vardır.",
            "2. CIN II: Atipik hücreler epitelin alt 2/3'ünü istila eder.",
            "3. CIN III: Atipi tüm katları kaplar, tam kalınlık tutulur (Karsinoma in situ).",
            "4. Mikroinvazyon: Bazal membran delinirse lezyon invaziv karsinoma dönüşür."
        ]),
        make_recall("CIN II ve CIN III lezyonlarının epitel içindeki tutulum derinlikleri arasındaki temel fark nedir?", "CIN II epitelin alt 2/3'ünü tutarken; CIN III epitelin tam kalınlığını (tüm katlarını) tutar."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: HSIL Tutulum Derinliği", [
            {"text": "CIN II epitelin alt üçte ikisini tutar.", "isLie": False, "explanation": "Doğru. Tutulum alt 2/3'e uzanır."},
            {"text": "CIN III epitelin tam kalınlığını tutar ve olgunlaşma kaybolmuştur.", "isLie": False, "explanation": "Doğru. Tam kat displazidir."},
            {"text": "CIN III tanısı için atipik hücrelerin mutlaka karaciğer ve beyne metastaz yapması şarttır.", "isLie": True, "explanation": "Tuzak! CIN III intraepitelyal bir lezyondur, bazal membranı aşmamıştır; uzak metastaz yapmaz."},
            {"text": "HSIL grubu CIN II ve CIN III lezyonlarını içerir.", "isLie": False, "explanation": "Doğru. Yüksek dereceli sınıflamadır."}
        ]),
        make_quiz("Epitelin tam kalınlığını tutan ve skuamöz matürasyonun tamamen kaybolduğu servikal intraepitelyal lezyon hangisidir?", [
            {"key": "A", "text": "CIN III (HSIL)", "isCorrect": True, "explanation": "CIN III epitelin tam kalınlığını tutar (karsinoma in situ)."},
            {"key": "B", "text": "CIN I (LSIL)", "isCorrect": False, "explanation": "CIN I sadece alt 1/3'ü tutar."},
            {"key": "C", "text": "Yalnızca Bartholin kisti", "isCorrect": False, "explanation": "Benign vulvar kisttir."},
            {"key": "D", "text": "Normal vajinal mukoza", "isCorrect": False, "explanation": "Normale tam kat atipi denmez."}
        ])
    ]
    slides.append(make_slide(37, "HSIL (CIN II ve CIN III): Tanım ve Tutulum Derinliği", "CIN II (alt 2/3), CIN III (tam kalınlık), matürasyon kaybı ve intraepitelyal yayılım", "Preinvaziv Histopatoloji: HSIL", s37_narrative, s37_bullets, s37_elements))

    # Slide 38: HSIL Histopatolojisi: Polarite Kaybı ve Atipik Mitozlar
    s38_narrative = (
        "HSIL (CIN II-III) biyopsilerinde mikroskop altında gözlenen hücresel ve mimari bozulmalar, "
        "lezyonun malign transformasyon potansiyelini açıkça ortaya koyar.\n\n"
        "- **Polarite Kaybı:** Normal skuamöz epitelde hücreler bazalden yüzeye doğru yataylaşarak düzenli sıralanırken, "
        "HSIL'de hücresel yönelim tamamen bozulur; hücreler birbirinin üzerine yığılmış kaotik bir görünüm alır.\n"
        "- **Nükleer Pleomorfizm:** Çekirdek/sitoplazma oranı belirgin artmıştır; nükleuslar ileri derecede hiperkromatik, "
        "düzensiz konturlu ve iri kromatin topakları barındırır.\n"
        "- **Atipik Mitozlar:** Normalde mitoz sadece bazal tabakada görülürken; HSIL'de **epitelin üst katmanlarında** "
        "ve sıklıkla **anormal/atipik mitotik figürler (tripolar/tetrapolar mitoz)** saptanır.\n"
        "- **Koilositoz Yokluğu:** ==CIN III'te koilositik değişiklik genellikle yoktur==; çünkü hücreler olgunlaşamadığı için virüs kapsid montajı yapamaz.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] CIN III'te atipik mitozlar üst katmanlara yayılır, polarite kaybolur ve hücreler olgunlaşamadığı için koilositik değişiklik genellikle görülmez."
    )
    s38_bullets = [
        "Hücresel polarite ve tabakalaşma düzeni tamamen kaybolur.",
        "Epitelin üst katmanlarında anormal ve atipik mitozlar izlenir.",
        "CIN III lezyonlarında koilositik değişiklik genellikle bulunmaz."
    ]
    s38_elements = [
        make_cloze("CIN III lezyonunda epitel olgunlaşması durduğu için koilositik değişiklik genellikle izlenmez.", "koilositik", "Aktif viral kapsid montajını gösteren halo hücresi"),
        make_table("HSIL ve CIN III Mikroskobik Bulguları", ["Histopatolojik Belirteç", "Morfolojik Özellik", "Biyolojik Anlam"], [
            {"cells": [{"text": "Mitoz Dağılımı", "isMasked": False}, {"text": "Orta ve üst katmanlarda atipik mitozlar", "isMasked": True, "hint": "anormal bölünme figürleri"}, {"text": "Kontrolsüz hücresel proliferasyon"}]},
            {"cells": [{"text": "Koilositoz Varlığı", "isMasked": False}, {"text": "Genellikle yoktur veya kaybolmuştur", "isMasked": False}, {"text": "Epitel olgunlaşamadığından virüs üretilemez", "isMasked": True, "hint": "kapsid montaj yetersizliği"}]}
        ]),
        make_chain("HSIL Morfolojik Dönüşüm Zinciri", [
            "1. E6/E7 Aşırı Salımı: Hücreler sürekli bölünme döngüsünde kilitli kalır.",
            "2. Polarite Kaybı: Hücrelerin yataylaşma ve bazal-apikal ekseni çöker.",
            "3. Anormal Mitozlar: Genomik kırıklar nedeniyle çok kutuplu mitozlar belirir.",
            "4. Matürasyon Durması: Hücreler yüzeye kadar olgunlaşamaz ve koilositoz silinir."
        ]),
        make_recall("CIN III lezyonlarında CIN I'in aksine koilositik değişikliğin genellikle görülmemesinin nedeni nedir?", "Epitel olgunlaşmasının tamamen durması nedeniyle virüsün kapsid sentezini ve montajını tamamlayamamasıdır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: HSIL Histopatolojisi", [
            {"text": "CIN III'te hücresel polarite ve yönelim bozulur.", "isLie": False, "explanation": "Doğru. Kaotik bir mimari izlenir."},
            {"text": "Epitelin orta ve üst katmanlarında atipik mitozlar görülebilir.", "isLie": False, "explanation": "Doğru. Mitoz bazali aşarak yukarı tırmanır."},
            {"text": "CIN III lezyonlarında tüm hücreler bol süt salgılayan sekretuar asinuslara dönüşür.", "isLie": True, "explanation": "Tuzak! CIN III skuamöz displazidir; meme benzeri süt salgısı yapmaz."},
            {"text": "CIN III'te koilositik değişiklik genellikle bulunmaz.", "isLie": False, "explanation": "Doğru. Diferansiyasyon olmadığı için koilositoz silinir."}
        ]),
        make_quiz("CIN III histopatolojisinde koilositik değişiklik ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?", [
            {"key": "A", "text": "CIN III'te hücre olgunlaşması durduğu için koilositik değişiklik genellikle yoktur", "isCorrect": True, "explanation": "Diferansiyasyon durduğu için koilositoz genellikle izlenmez."},
            {"key": "B", "text": "Tümör dokusunun %100'ü dev koilositlerden meydana gelir", "isCorrect": False, "explanation": "Koilosit CIN III'te kaybolur."},
            {"key": "C", "text": "Koilositler kemik hücrelerine yapışarak osteomiyelit yapar", "isCorrect": False, "explanation": "Kemikle ilgisi yoktur."},
            {"key": "D", "text": "Koilosit yalnızca erkek spermlerinde bulunan bir yapıdır", "isCorrect": False, "explanation": "Skuamöz epitel hücresidir."}
        ])
    ]
    slides.append(make_slide(38, "HSIL Histopatolojisi: Polarite Kaybı ve Atipik Mitozlar", "Nükleer pleomorfizm, üst katman mitozları, koilositoz yokluğu ve hücresel kaos", "Histopatolojik Kriterler", s38_narrative, s38_bullets, s38_elements))

    # Slide 39: HSIL'in Doğal Seyri ve İnvaziv Karsinoma İlerleme
    s39_narrative = (
        "HSIL (CIN II-III), yüksek malign potansiyel taşıyan ve tedavi edilmediği takdirde invaziv "
        "karsinoma ilerleme riski belirgin olan bir lezyondur.\n\n"
        "- **Doğal Seyir Dağılımı:** Tedavi edilmeyen HSIL olgularının **yaklaşık %30'u geriler**, "
        "**%60'ı sebat eder (persiste kalır)** ve **%10'u invaziv karsinoma ilerler**.\n"
        "- **İlerleme Süresi:** HSIL zemininden invaziv serviks karsinomuna geçiş ani olmayıp genellikle "
        "**2 ila 10 yıllık** bir zaman diliminde kademeli mutasyon birikimiyle gerçekleşir.\n"
        "- **De Novo Gelişim:** HSIL'lerin çoğu LSIL'den evrilmekle birlikte, bazı yüksek riskli olgular "
        "öncesinde LSIL evresi olmaksızın doğrudan (de novo) da ortaya çıkabilir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] HSIL vakalarının %30'u geriler, %60'ı persiste kalır, %10'u karsinoma ilerler; ilerleme 2-10 yıl içinde gerçekleşir."
    )
    s39_bullets = [
        "HSIL vakalarının %30'u geriler, %60'ı persiste kalır.",
        "Yaklaşık %10'u invaziv karsinoma ilerler.",
        "İnvaziv karsinoma geçiş 2 ila 10 yıl içinde gerçekleşir."
    ]
    s39_elements = [
        make_cloze("HSIL lezyonlarının invaziv karsinoma ilerleme süreci genellikle 2 ila 10 yıl içinde gerçekleşir.", "2 ila 10 yıl", "İnvaziv kansere dönüşüm için gereken süre aralığı"),
        make_table("HSIL Doğal Seyir Dinamikleri", ["Klinik Seyir", "Görülme Oranı", "Zamanlama / Karakter"], [
            {"cells": [{"text": "Spontan Regresyon", "isMasked": False}, {"text": "%30", "isMasked": True, "hint": "üçte bir oranında gerileme"}, {"text": "İmmünite ile gerileyebilir"}]},
            {"cells": [{"text": "Persistans (Sebat)", "isMasked": False}, {"text": "%60", "isMasked": False}, {"text": "Yıllarca stabil kalabilir", "isMasked": True, "hint": "uzun süreli sebat"}]},
            {"cells": [{"text": "İnvaziv Karsinoma İlerleme", "isMasked": False}, {"text": "%10", "isMasked": True, "hint": "kanserleşen hasta fraksiyonu"}, {"text": "2-10 yıl içinde bazal membran aşılır"}]}
        ]),
        make_chain("HSIL'den İnvaziv Karsinoma Geçiş", [
            "1. HSIL Kuruluşu: CIN II/III evresinde tam kata yakın genetik instabilite oluşur.",
            "2. Yıllar Süren Persistans: Lezyon 2-10 yıl boyunca epitel içinde sebat eder.",
            "3. Ek Mutasyon Birikimi: Sigara veya kofaktörlerle ek onkojenik mutasyonlar eklenir.",
            "4. Stromal İnvazyon: Bazal membran proteolitik olarak delinerek invaziv karsinom başlar."
        ]),
        make_recall("HSIL olgularında invaziv karsinoma ilerleme oranı ve bu ilerlemenin gerçekleştiği ortalama süre nedir?", "İlerleme oranı yaklaşık %10'dur ve genellikle 2 ila 10 yıllık bir sürede gerçekleşir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: HSIL Doğal Seyri", [
            {"text": "HSIL vakalarının yaklaşık %10'u invaziv karsinoma ilerler.", "isLie": False, "explanation": "Doğru. Kanserleşme oranı %10'dur."},
            {"text": "HSIL'den karsinoma ilerleme genellikle 2-10 yıl içinde gerçekleşir.", "isLie": False, "explanation": "Doğru. Süreç yıllar alır."},
            {"text": "HSIL teşhisi konan hastaların %100'ü 5 dakika içinde anaplastik metastatik şoka girer.", "isLie": True, "explanation": "Tuzak! Süreç yavaş seyreder; %30'u geriler, %60'ı persiste eder, kansere geçiş 2-10 yıl sürer."},
            {"text": "HSIL lezyonlarının bir kısmı öncesinde LSIL olmaksızın de novo gelişebilir.", "isLie": False, "explanation": "Doğru. De novo gelişim mümkündür."}
        ]),
        make_quiz("HSIL (CIN II-III) lezyonlarının tedavi edilmediğinde invaziv karsinoma ilerleme oranı ve süresi nasıldır?", [
            {"key": "A", "text": "Yaklaşık %10 oranında ve 2 ila 10 yıl içinde", "isCorrect": True, "explanation": "HSIL'in %10'u 2-10 yılda karsinoma ilerler."},
            {"key": "B", "text": "Olguların %100'ünde 24 saat içinde", "isCorrect": False, "explanation": "Süreç akut değildir."},
            {"key": "C", "text": "Hiçbir zaman ilerlemez, daima %100 geriler", "isCorrect": False, "explanation": "Prekanserözdür, ilerleme riski %10'dur."},
            {"key": "D", "text": "Sadece erkeklerde 50 yıl sonra", "isCorrect": False, "explanation": "Kadın serviks patolojisidir."}
        ])
    ]
    slides.append(make_slide(39, "HSIL'in Doğal Seyri ve İnvaziv Karsinoma İlerleme", "Regresyon (%30), persistans (%60), progresyon (%10), 2-10 yıllık pencere", "Doğal Seyir ve Kanser Riski", s39_narrative, s39_bullets, s39_elements))

    # Slide 40: [TEKRAR SAYFASI - CHECKPOINT 4] Genom Entegrasyonu ve SIL/CIN Spektrumu
    s40_narrative = (
        "Bölüm 4'te viral genomun moleküler durumunu, E2 gen bütünlüğünün kırılmasını ve prekanseröz "
        "lezyonların (LSIL/CIN I ve HSIL/CIN II-III) histopatolojik spektrumunu inceledik.\n\n"
        "- **Genom Entegrasyonu ve E2:** Yüksek riskli HPV DNA'sı **insan genomuna entegre olur**; "
        "bu sırada **E2 repressör geni parçalanır** ve E6/E7 onkoprotein ekspresyonu kontrolsüzce katlanır.\n"
        "- **LSIL (CIN I) Karakteri:** Atipi **alt 1/3'e sınırlıdır**; üst katmanlarda **koilositik halo** belirgindir; "
        "vakaların **%60'ı spontan gerilediğinden** prekanseröz kabul edilmez.\n"
        "- **HSIL (CIN II-III) Karakteri:** CIN II alt 2/3'ü, CIN III **tam kalınlığı** tutar; hücresel polarite kaybolur, "
        "üst katmanlarda atipik mitozlar belirir ve olgunlaşma durduğu için **koilositoz genellikle yoktur**.\n"
        "- **İlerleme Dinamiği:** HSIL'in %10'u **2-10 yıl içinde** invaziv karsinoma ilerler.\n\n"
        "> [!IMPORTANT]\n"
        "> [BÖLÜM 4 SENTEZİ] Entegrasyon E2'yi kırarak E6/E7 fırtınası yaratır; LSIL alt 1/3'te koilositli ve selim seyrederken, HSIL tam kata varan atipi ve atipik mitozlarla invaziv kanserin gerçek öncülüdür."
    )
    s40_bullets = [
        "Entegrasyon E2 repressörünü kırarak frensiz E6/E7 üretimi sağlar.",
        "LSIL alt 1/3'ü tutar, koilositoz vardır, %60 geriler (prekanseröz sayılmaz).",
        "HSIL alt 2/3 veya tam katı tutar, atipik mitozlar vardır, %10'u 2-10 yılda kansere gider."
    ]
    s40_elements = [
        make_cloze("Bölüm 4 sentezinde incelenen ve atipinin epitelin tam kalınlığını tuttuğu ağır lezyon CIN III olarak tanımlanır.", "CIN III", "Bölüm 4 checkpointinde pekiştirilen tam kat displazi"),
        make_table("Bölüm 4 SIL ve CIN Kapsamlı Karşılaştırması", ["Özellik", "LSIL (CIN I)", "HSIL (CIN II-III)"], [
            {"cells": [{"text": "Tutulum Derinliği", "isMasked": False}, {"text": "Epitel alt 1/3 tabakası", "isMasked": False}, {"text": "Alt 2/3 veya tam kalınlık", "isMasked": True, "hint": "derin veya tam kat yayılım"}]},
            {"cells": [{"text": "Koilositik Değişiklik", "isMasked": False}, {"text": "Yüzeysel katmanlarda belirgin", "isMasked": True, "hint": "belirgin perinükleer halo"}, {"text": "CIN III'te genellikle yoktur", "isMasked": False}]},
            {"cells": [{"text": "Doğal Seyir", "isMasked": False}, {"text": "%60 spontan geriler", "isMasked": False}, {"text": "%10 karsinoma ilerler (2-10 yıl)", "isMasked": True, "hint": "malign progresyon oranı"}]}
        ]),
        make_chain("Bölüm 4 Mekanizma Bütünleştirmesi", [
            "1. Genomik Kırılma: HPV 16/18 DNA'sı E2 genini yıkarak konak DNA'sına entegre olur.",
            "2. CIN I Evresi: Erken dönemde alt 1/3'te hafif displazi ve bol koilositoz izlenir.",
            "3. CIN III Evresi: Polarite çöker, tam kalınlık atipik hücreyle dolar, koilositler silinir.",
            "4. Kanser Eşiği: 2 ila 10 yıl içinde bazal membran delinecek aşamaya ulaşılır."
        ]),
        make_recall("Bölüm 4'te öğrendiğimiz: (1) Entegrasyonla parçalanan repressör gen ve (2) CIN III'te bulunmayan viral morfolojik bulgu nedir?", "(1) E2 repressör geni, (2) Koilositik değişikliktir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Bölüm 4 Checkpoint Sentezi", [
            {"text": "Viral entegrasyon E2 genini bozar ve E6/E7 üretimini artırır.", "isLie": False, "explanation": "Doğru. Temel regülasyon kırılmasıdır."},
            {"text": "LSIL'in %60'ı spontan geriler, bu nedenle prekanseröz sayılmaz.", "isLie": False, "explanation": "Doğru. Biyolojik regresyon özelliğidir."},
            {"text": "CIN III lezyonlarında hücreler tamamen olgunlaşıp dev koilosit tabakaları yapar.", "isLie": True, "explanation": "Tuzak! CIN III'te olgunlaşma durduğu için koilositik değişiklik genellikle yoktur."},
            {"text": "HSIL vakalarının yaklaşık %10'u 2-10 yıl içinde karsinoma ilerler.", "isLie": False, "explanation": "Doğru. Malignite progresyon oranıdır."}
        ]),
        make_quiz("Bölüm 4'te pekiştirilen SIL ve CIN sınıflaması ile ilgili aşağıdaki ifadelerden hangisi YANLIŞTIR?", [
            {"key": "A", "text": "CIN I epitelin tam kalınlığını tutarken CIN III yalnızca alt 1/3'ünü tutar", "isCorrect": True, "explanation": "Tam tersi! CIN I alt 1/3'ü, CIN III tam kalınlığı tutar."},
            {"key": "B", "text": "Viral entegrasyonda E2 geninin kırılması E6 ve E7'yi artırır", "isCorrect": False, "explanation": "Doğru mekanizmadır."},
            {"key": "C", "text": "LSIL lezyonlarının yaklaşık %60'ı kendiliğinden geriler", "isCorrect": False, "explanation": "Doğru bilgidir."},
            {"key": "D", "text": "HSIL'den invaziv karsinoma geçiş 2-10 yıl sürebilir", "isCorrect": False, "explanation": "Doğru bilgidir."}
        ])
    ]
    slides.append(make_slide(40, "[TEKRAR SAYFASI - CHECKPOINT 4] Genom Entegrasyonu ve SIL/CIN Spektrumu", "Bölüm 4 kapsamlı tekrarı: E2 kırılması, CIN I-III mimarisi, koilositoz ve doğal seyir", "Bölüm Tekrarı ve Konsolidasyon", s40_narrative, s40_bullets, s40_elements))

    return slides

if __name__ == '__main__':
    slides = get_sec4()
    print(f"Sec4 generated: {len(slides)} slides (Slide 31 to 40)")
    for s in slides:
        print(f" - Slide {s['slideNumber']}: {s['title']} ({len(s['interactiveElements'])} elements, {len(s['content'].split())} words)")
