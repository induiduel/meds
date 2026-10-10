import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from meds.scripts.deck_generators.builder_helper import make_slide, make_cloze, make_table, make_chain, make_recall, make_spot_lie, make_quiz

def get_sec6():
    slides = []

    # Slide 51: HPV DNA Testi ve Pap Smear Tamamlayıcılığı
    s51_narrative = (
        "Modern servikal kanser tarama protokollerinde Pap smear sitolojisinin yanına güçlü bir moleküler "
        "araç olarak **HPV DNA testi** eklenmiş ve ko-test konsepti oluşturulmuştur.\n\n"
        "- **Yüksek Duyarlılık:** HPV DNA testleri, servikal sürüntüde yüksek riskli onkojenik HPV tiplerinin "
        "genomik varlığını nükleik asit amplifikasyonu (PCR vb.) ile **son derece yüksek hassasiyetle** saptar.\n"
        "- **Mükemmel Tamamlayıcılık:** Sitoloji hücresel morfolojik hasarı gösterirken, HPV DNA testi etyolojik "
        "ajanın varlığını ortaya koyar; ikisinin birlikte kullanımı (ko-test) tarama güvenilirliğini zirveye taşır.\n"
        "- **Yalancı Negatiflik Azalması:** Pap smearin tek başına gösterebileceği örnekleme hataları HPV testi ile telafi edilir.\n\n"
        "> [!NOTE]\n"
        "> HPV DNA testi servikal sürüntüde yüksek riskli HPV tiplerini saptamada çok hassastır ve Pap testini tamamlar."
    )
    s51_bullets = [
        "HPV DNA testi yüksek riskli virüs tiplerini saptamada çok hassastır.",
        "Pap smear sitolojisine güçlü bir tamamlayıcı testtir.",
        "Moleküler duyarlılık sayesinde atlanan displazileri yakalar."
    ]
    s51_elements = [
        make_cloze("HPV DNA testi servikal sürüntüde yüksek riskli viral genotipleri saptamada çok hassas bir yöntemdir.", "yüksek riskli", "Kanser yapıcı HPV tipleri grubu"),
        make_table("Pap Smear ve HPV DNA Testi Karşılaştırması", ["Özellik", "Pap Smear (Sitoloji)", "HPV DNA Testi (Moleküler)"], [
            {"cells": [{"text": "İncelenen Unsur", "isMasked": False}, {"text": "Hücresel morfoloji ve nükleus atipisi", "isMasked": True, "hint": "mikroskobik hücre görüntüsü"}, {"text": "Viral nükleik asit dizilimi"}]},
            {"cells": [{"text": "Duyarlılık / Özgüllük", "isMasked": False}, {"text": "Orta duyarlılık, yüksek özgüllük", "isMasked": False}, {"text": "Çok yüksek duyarlılık, orta özgüllük", "isMasked": True, "hint": "yüksek hassasiyetli yakalama gücü"}]}
        ]),
        make_chain("Ko-Test Entegrasyonu", [
            "1. Tek Sürüntü: Servikal transformasyon bölgesinden tek bir fırça ile örnek alınır.",
            "2. İkili Analiz: Sıvı bazlı materyalden hem mikroskopi lamı hazırlanır hem DNA ekstrakte edilir.",
            "3. Çift Doğrulama: Sitolojide atipi aranırken, PCR ile yüksek riskli tipler sorgulanır.",
            "4. Maksimum Güvenlik: Her iki testin negatifliği kadına 5 yıllık güvenli pencere sağlar."
        ]),
        make_recall("Servikal kanser taramasında HPV DNA testinin Pap smear testine kıyasla en belirgin avantajı nedir?", "Yüksek riskli onkojenik HPV tiplerini saptamada moleküler duyarlılığının (sensitivitesinin) çok daha yüksek olmasıdır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: HPV DNA Testi", [
            {"text": "HPV DNA testi servikal sürüntüde yüksek riskli tipleri saptamada çok hassastır.", "isLie": False, "explanation": "Doğru. Duyarlılığı son derece yüksektir."},
            {"text": "HPV testi Pap smear sitolojisine mükemmel bir tamamlayıcıdır.", "isLie": False, "explanation": "Doğru. Birlikte ko-test olarak kullanılırlar."},
            {"text": "HPV DNA testi hastaya genel anestezi altında yapılan açık beyin ameliyatı ile alınır.", "isLie": True, "explanation": "Tuzak! Test poliklinikte ağrısız servikal sürüntü fırçasıyla alınır; beyin cerrahisiyle ilgisi yoktur."},
            {"text": "Yüksek riskli tiplerin genomik varlığını PCR yöntemleriyle inceler.", "isLie": False, "explanation": "Doğru. Moleküler amplifikasyon testidir."}
        ]),
        make_quiz("Servikal sürüntüde yüksek riskli onkojenik HPV tiplerini saptamada son derece hassas olan tarama yöntemi nedir?", [
            {"key": "A", "text": "HPV DNA testi", "isCorrect": True, "explanation": "HPV DNA testi moleküler olarak yüksek riskli tipleri yakalar."},
            {"key": "B", "text": "Kanda ürik asit ölçümü", "isCorrect": False, "explanation": "Gut hastalığı testidir."},
            {"key": "C", "text": "Akciğer grafisi", "isCorrect": False, "explanation": "Toraks radyolojisidir."},
            {"key": "D", "text": "Dışkıda gizli kan arama", "isCorrect": False, "explanation": "Kolorektal taramadır."}
        ])
    ]
    slides.append(make_slide(51, "HPV DNA Testi ve Pap Smear Tamamlayıcılığı", "Moleküler tarama, yüksek analitik duyarlılık, ko-test ve sitoloji tamamlayıcılığı", "Moleküler Tarama", s51_narrative, s51_bullets, s51_elements))

    # Slide 52: HPV DNA Testinin Yaş Gruplarına Göre Değeri (≥30 Yaş)
    s52_narrative = (
        "HPV DNA testinin tarama aracı olarak klinik etkinliği ve pozitif öngörü değeri, hastanın yaşına "
        "bağlı olarak dramatik bir değişkenlik sergiler.\n\n"
        "- **Genç Kadınlarda Durum (<30 Yaş):** 30 yaşın altındaki cinsel aktif genç kadınlarda HPV enfeksiyon "
        "insidansı son derece yüksektir; ancak bu enfeksiyonların %80-90'ı geçici olduğundan, testin **pozitif "
        "öngörü değeri düşüktür** ve gereksiz anksiyete ile gereksiz biyopsilere yol açar.\n"
        "- **30 Yaş ve Üzeri Kadınlar (≥30 Yaş):** 30 yaşından sonra geçici enfeksiyon insidansı düşer; bu yaşta "
        "saptanan pozitiflikler sıklıkla **persistan enfeksiyonu** gösterir; bu nedenle test **özellikle 30 yaş "
        "ve üzerindeki kadınlarda son derece değerlidir**.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] HPV DNA testi özellikle 30 yaş ve üzerindeki kadınlarda taramada değerlidir; gençlerde geçici enfeksiyon sıklığı nedeniyle prediktif değeri düşüktür."
    )
    s52_bullets = [
        "HPV DNA testi özellikle 30 yaş ve üzerindeki kadınlarda değerlidir.",
        "Gençlerde (<30 yaş) enfeksiyon çok sık ve geçici olduğundan değeri düşüktür.",
        "İleri yaşta pozitiflik persistan enfeksiyonu ve displazi riskini yansıtır."
    ]
    s52_elements = [
        make_cloze("HPV DNA testi karsinogenez taramasında özellikle 30 yaş ve üzeri kadınlarda yüksek klinik değere sahiptir.", "30 yaş", "HPV DNA testinin rutin taramada en değerli olduğu eşik yaş"),
        make_table("Yaş Gruplarına Göre HPV DNA Testinin Karakteri", ["Yaş Grubu", "Enfeksiyon Karakteri", "Testin Taramadaki Değeri"], [
            {"cells": [{"text": "Gençler (<30 yaş)", "isMasked": False}, {"text": "Yüksek insidans, %80-90 geçici klirens", "isMasked": True, "hint": "sık fakat geçici viral temas"}, {"text": "Düşük prediktif değer (rutin önerilmez)"}]},
            {"cells": [{"text": "Erişkinler (≥30 yaş)", "isMasked": False}, {"text": "Kalıcı persistan enfeksiyon odakları", "isMasked": False}, {"text": "Çok yüksek prediktif değer (altın standart)", "isMasked": True, "hint": "yüksek klinik karar değeri"}]}
        ]),
        make_chain("Yaşa Göre Tarama Dinamiği", [
            "1. 20'li Yaşlar: Yüksek bulaş oranı vardır; bağışıklık sistemi virüsleri hızla temizler.",
            "2. Gençte Test Yanıltması: Test pozitif çıkar fakat kansere gitmez, gereksiz panik yaratır.",
            "3. 30 Yaş Eşiği: İmmün klirensi tamamlayamayan persistan virüsler sahnede kalır.",
            "4. Hedefe Yönelik Tarama: 30 yaş üstünde yapılan test gerçek risk altındaki kadınları yakalar."
        ]),
        make_recall("HPV DNA testi rutin taramada hangi yaş grubunda en yüksek klinik değere sahiptir ve gençlerde neden önerilmez?", "30 yaş ve üzerindeki kadınlarda değerlidir; gençlerde geçici enfeksiyon oranı çok yüksek olduğundan prediktif değeri düşüktür."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: HPV Testi ve Yaş Grupları", [
            {"text": "HPV DNA testi özellikle 30 yaş ve üzeri kadınlarda değerlidir.", "isLie": False, "explanation": "Doğru. Persistan enfeksiyonu gösterir."},
            {"text": "Gençlerde HPV enfeksiyon sıklığı yüksek fakat çoğu geçicidir.", "isLie": False, "explanation": "Doğru. %80-90'ı kendiliğinden geçer."},
            {"text": "HPV DNA testi sadece 1 yaşındaki bebeklerde süt dişlerini saymak için kullanılır.", "isLie": True, "explanation": "Tuzak! HPV testi diş saymaz; servikal sürüntüde viral DNA arar ve 30 yaş üstünde değerlidir."},
            {"text": "Genç kadınlarda testin pozitif öngörü değeri düşüktür.", "isLie": False, "explanation": "Doğru. Geçici pozitiflik yanıltabilir."}
        ]),
        make_quiz("HPV DNA testinin rutin servikal kanser taramasında en değerli ve anlamlı olduğu yaş grubu hangisidir?", [
            {"key": "A", "text": "30 yaş ve üzerindeki kadınlar", "isCorrect": True, "explanation": "HPV DNA testi ≥30 yaş kadınlarda persistan lezyonları saptamada en değerlidir."},
            {"key": "B", "text": "Yalnızca 10-14 yaş arası ilkokul çocukları", "isCorrect": False, "explanation": "Bu yaşta tarama yapılmaz."},
            {"key": "C", "text": "Sadece 90 yaş üzerindeki hastalar", "isCorrect": False, "explanation": "Tarama yaşı 65'te genellikle sonlandırılır."},
            {"key": "D", "text": "Doğumdan hemen sonraki ilk 24 saat", "isCorrect": False, "explanation": "Yenidoğanda yapılmaz."}
        ])
    ]
    slides.append(make_slide(52, "HPV DNA Testinin Yaş Gruplarına Göre Değeri (≥30 Yaş)", "30 yaş eşiği, geçici enfeksiyon yanılgısı, persistan odak yakalama ve prediktif değer", "Yaş Grupları ve Tarama Stratejisi", s52_narrative, s52_bullets, s52_elements))

    # Slide 53: HPV DNA Negatifliğinin 5 Yıllık Güvencesi
    s53_narrative = (
        "HPV DNA testinin en güçlü klinik yönlerinden biri, son derece yüksek olan **negatif öngörü değeridir** "
        "(negative predictive value).\n\n"
        "- **Mükemmel Güvenlik:** 30 yaş ve üzerindeki bir kadında yüksek riskli HPV DNA testi **negatif çıktığında**, "
        "bu kadında izleyen **5 yıl içinde servikal neoplazi (CIN II/III veya karsinom) gelişme riski son derece düşüktür**.\n"
        "- **Tarama Aralıklarının Uzaması:** Bu biyolojik gerçeklik, sağlık otoritelerinin tarama aralığını her yıl "
        "yapılan smearlerden **5 yılda bir yapılan HPV / ko-test taramalarına** uzatmasına olanak tanımıştır.\n"
        "- **Klinik Rahatlama:** Negatif test sonucu hem hastaya hem hekime uzun süreli güvenli bir takip konforu sunar.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Yüksek riskli HPV testi negatif olan bir kadında izleyen 5 yılda servikal neoplazi riski çok düşüktür; tarama aralığı 5 yıla uzatılabilir."
    )
    s53_bullets = [
        "Yüksek riskli HPV negatifse izleyen 5 yılda neoplazi riski çok düşüktür.",
        "Yüksek negatif prediktif değer tarama aralığını 5 yıla uzatır.",
        "Gereksiz sık tarama ve girişimlerin önüne geçer."
    ]
    s53_elements = [
        make_cloze("Yüksek riskli HPV testi negatif sonuçlanan kadınlarda izleyen 5 yıl içinde neoplazi riski son derece düşüktür.", "5 yıl", "Negatif HPV testinin sağladığı güvenli süre penceresi"),
        make_table("HPV Test Sonucu ve 5 Yıllık Klinik Risk", ["HPV Test Sonucu", "5 Yıllık Neoplazi Riski", "Önerilen Tarama Aralığı"], [
            {"cells": [{"text": "Yüksek Riskli HPV Negatif", "isMasked": False}, {"text": "Son derece düşük (<%0.1)", "isMasked": True, "hint": "ihmal edilebilir minimum düzey"}, {"text": "5 yılda bir güvenli tarama"}]},
            {"cells": [{"text": "Yüksek Riskli HPV Pozitif", "isMasked": False}, {"text": "Artmış displazi riski", "isMasked": False}, {"text": "Sitoloji veya 1 yıl sonra tekrar kontrol", "isMasked": True, "hint": "yakın takip veya ileri tetkik"}]}
        ]),
        make_chain("Negatif Testten Uzatılmış Taramaya", [
            "1. Rutin Ko-Test: 35 yaşındaki kadından servikal HPV sürüntüsü alınır.",
            "2. Moleküler Rapor: Yüksek riskli tüm HPV tipleri negatif olarak raporlanır.",
            "3. Düşük Risk Kanıtı: Epitelde onkojenik virüs bulunmadığından neoplazi gelişemez.",
            "4. 5 Yıllık Güvence: Hastanın bir sonraki taraması 5 yıl sonrasına randevulanır."
        ]),
        make_recall("Yüksek riskli HPV DNA testi negatif gelen 30 yaş üstü bir kadında neoplazi riski açısından izleyen kaç yıl boyunca güvence sağlanır?", "İzleyen 5 yıl boyunca servikal neoplazi riski son derece düşüktür."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: HPV Testi Negatif Öngörü Değeri", [
            {"text": "Yüksek riskli HPV testi negatifse 5 yılda servikal neoplazi riski çok düşüktür.", "isLie": False, "explanation": "Doğru. Negatif prediktif değeri çok yüksektir."},
            {"text": "Bu güvence tarama aralıklarının 5 yıla uzatılmasını sağlamıştır.", "isLie": False, "explanation": "Doğru. Uluslararası kılavuzlar 5 yılı benimser."},
            {"text": "HPV testi negatif çıkan bir kadın ertesi sabah kesinlikle tümörden yaşamını yitirir.", "isLie": True, "explanation": "Tuzak! Negatif test kadının 5 yıl boyunca en güvende olduğu anlamına gelir."},
            {"text": "Negatif sonuç hastaya uzun süreli klinik güvence verir.", "isLie": False, "explanation": "Doğru. Güvenli takip penceresidir."}
        ]),
        make_quiz("Yüksek riskli HPV testi negatif olan bir kadında izleyen süreçteki neoplazi riski ile ilgili aşağıdakilerden hangisi DOĞRUDUR?", [
            {"key": "A", "text": "İzleyen 5 yılda servikal neoplazi riski son derece düşüktür", "isCorrect": True, "explanation": "Testin negatifliği 5 yıllık güçlü bir koruyucu öngörü sağlar."},
            {"key": "B", "text": "İzleyen 24 saat içinde lezyonun kanserleşmesi zorunludur", "isCorrect": False, "explanation": "Virüs yoksa neoplazi riski yoktur."},
            {"key": "C", "text": "Test hiçbir bilgi vermez, tamamen yazı-tura atmaktan ibarettir", "isCorrect": False, "explanation": "Bilimsel kanıtı en güçlü tarama testidir."},
            {"key": "D", "text": "Hastaya hemen acil açık ameliyat yapılması gerekir", "isCorrect": False, "explanation": "Girişim gerekmez, rutin takip 5 yıl sonradır."}
        ])
    ]
    slides.append(make_slide(53, "HPV DNA Negatifliğinin 5 Yıllık Güvencesi", "Yüksek negatif prediktif değer, 5 yıllık güvenlik penceresi ve uzatılmış tarama", "Klinik Öngörü ve Takip", s53_narrative, s53_bullets, s53_elements))

    # Slide 54: HPV Aşılaması: Primer Korunmanın Temeli
    s54_narrative = (
        "Tarama programları kanseri öncül evrede yakalayan ikincil koruma sağlarken, "
        "**HPV aşılaması enfeksiyonu başlamadan önleyen primer korunmanın ana basamağıdır**.\n\n"
        "- **Rekombinant VLP Teknolojisi:** HPV aşıları canlı veya zayıflatılmış virüs içermez; "
        "virüsün majör L1 kapsid proteininin rekombinant olarak üretilmesiyle elde edilen "
        "**virüs benzeri parçacıklardan (VLP - Virus-Like Particles)** oluşur.\n"
        "- **İmmünojenite:** VLP'ler enfeksiyöz değildir ve viral DNA içermez; ancak bağışıklık sistemine "
        "gerçek virüs gibi görünerek çok güçlü nötralizan antikor yanıtı oluştururlar.\n"
        "- **Primer Hedef:** Aşılama ile genital siğil, servikal öncü lezyonlar (CIN) ve invaziv karsinom "
        "sıklığının toplum düzeyinde dramatik şekilde azaltılması hedeflenir.\n\n"
        "> [!NOTE]\n"
        "> Yüksek riskli HPV tiplerine karşı aşılama, servikal kanserin önlenmesinde primer korunmanın en temel basamağıdır."
    )
    s54_bullets = [
        "HPV aşılaması primer (birincil) korunmanın temel taşıdır.",
        "L1 majör kapsid proteininden oluşan VLP teknolojisi kullanılır.",
        "Enfeksiyon riski taşımayan güçlü nötralizan antikorlar üretir."
    ]
    s54_elements = [
        make_cloze("HPV aşıları virüsün L1 kapsid proteininden üretilen rekombinant virüs benzeri parçacıklar teknolojisine dayanır.", "virüs benzeri parçacıklar", "VLP teknolojisinin Türkçe ifadesi"),
        make_table("HPV Aşısının İmmünolojik Yapısı", ["Komponent", "Aşı İçeriği", "Biyolojik Güvenlik / Sonuç"], [
            {"cells": [{"text": "Viral DNA Genomu", "isMasked": False}, {"text": "Aşıda kesinlikle bulunmaz", "isMasked": True, "hint": "genomik materyal yokluğu"}, {"text": "Enfeksiyon veya mutasyon riski sıfırdır"}]},
            {"cells": [{"text": "L1 Kapsid Proteini", "isMasked": False}, {"text": "Boş kapsid (VLP küresi)", "isMasked": False}, {"text": "Yüksek titrede nötralizan antikor sentezi", "isMasked": True, "hint": "koruyucu humoral bağışıklık"}]}
        ]),
        make_chain("Aşılama ile Korunma Mekanizması", [
            "1. Kas İçi Enjeksiyon: L1 VLP antijenleri deltoid kasa uygulanır.",
            "2. Plazma Hücresi Aktivasyonu: B lenfositler yüksek afiniteli anti-L1 IgG üretir.",
            "3. Servikal Mukozaya Geçiş: Antikorlar servikovajinal mukus sıvısına sızar.",
            "4. Nötralizasyon: Gerçek virüs geldiğinde antikorlar viriona yapışarak bazal hücreye girişini engeller."
        ]),
        make_recall("HPV aşılarının içeriğinde canlı virüs veya viral DNA bulunur mu ve koruyucu yapısı nedir?", "Hayır, viral DNA veya canlı virüs içermez; rekombinant L1 proteinlerinden oluşan virüs benzeri parçacıklardan (VLP) meydana gelir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: HPV Aşılaması İlkeleri", [
            {"text": "HPV aşısı servikal kanser önlenmesinde ana basamaktır.", "isLie": False, "explanation": "Doğru. Primer korunmanın temelidir."},
            {"text": "Aşılar L1 kapsid proteininden oluşan VLP yapısındadır.", "isLie": False, "explanation": "Doğru. Rekombinant VLP teknolojisidir."},
            {"text": "HPV aşısı canlı kuduz virüsü ile servikal dokuyu yakarak yok eden bir zehirdir.", "isLie": True, "explanation": "Tuzak! Kuduz virüsü veya doku yakımı ile ilgisi yoktur; rekombinant, güvenli ve son derece etkili bir aşıdır."},
            {"text": "Aşı viral DNA içermediğinden enfeksiyona yol açamaz.", "isLie": False, "explanation": "Doğru. Biyolojik olarak enfeksiyon yapamaz."}
        ]),
        make_quiz("HPV aşılarının biyolojik ve immünolojik içeriği aşağıdakilerden hangisidir?", [
            {"key": "A", "text": "Rekombinant L1 majör kapsid proteinlerinden oluşan virüs benzeri parçacıklar (VLP)", "isCorrect": True, "explanation": "HPV aşıları L1 proteini içeren VLP teknolojisiyle üretilir."},
            {"key": "B", "text": "Canlı ve zayıflatılmış ölümcül ebola virüsü", "isCorrect": False, "explanation": "Ebola ile ilgisi yoktur."},
            {"key": "C", "text": "Kemik iliğinden çekilmiş saf kalsiyum tozu", "isCorrect": False, "explanation": "İmmünolojik aşı proteinidir."},
            {"key": "D", "text": "Sadece şekerli serum fizyolojik", "isCorrect": False, "explanation": "Aktif VLP antijeni içerir."}
        ])
    ]
    slides.append(make_slide(54, "HPV Aşılaması: Primer Korunmanın Temeli", "Rekombinant VLP, L1 kapsid antijeni, enfeksiyöz olmayan yapı ve nötralizan antikorlar", "Primer Korunma: Aşı", s54_narrative, s54_bullets, s54_elements))

    # Slide 55: Aşı Hedef Yaş Grubu: 11-12 Yaş ve 26 Yaşa Kadar Yaklaşım
    s55_narrative = (
        "HPV aşısının en yüksek koruyuculuğu sağlayabilmesi için kişinin virüsle cinsel yolla karşılaşmasından "
        "önce uygulanması kritik kuraldır.\n\n"
        "- **Rutin Hedef Yaş:** Dünya Sağlık Örgütü ve uluslararası kılavuzlar aşılamanın **11-12 yaşındaki "
        "kız ve erkek çocuklara** rutin olarak yapılmasını önermektedir (9 yaştan itibaren başlanabilir).\n"
        "- **Erken Yaş Avantajı:** Erken yaşta uygulandığında bağışıklık sisteminin antikor üretme yanıtı erişkinlere "
        "göre çok daha güçlüdür (immün yanıt üstünlüğü).\n"
        "- **Yakalama (Catch-up) Aşılaması:** Önceden aşılanmamış olan bireylerde aşı **26 yaşına kadar "
        "genç kadın ve erkeklere** güvenle uygulanabilir ve yüksek koruma sağlar.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] HPV aşısı rutin olarak 11-12 yaşındaki kız ve erkek çocuklara önerilir; 26 yaşına kadar genç bireylere catch-up aşılaması yapılabilir."
    )
    s55_bullets = [
        "Aşılama rutin olarak 11-12 yaş kız ve erkek çocuklara önerilir.",
        "Cinsel aktivite öncesi yapıldığında koruyuculuk maksimumdur.",
        "26 yaşına kadar yakalama (catch-up) aşılaması uygulanabilir."
    ]
    s55_elements = [
        make_cloze("HPV aşısının rutin hedef popülasyonu 11-12 yaş kız ve erkek çocuklardır.", "11-12 yaş", "Rutin aşılamanın önerildiği ideal çocukluk yaş grubu"),
        make_table("HPV Aşılama Yaş Grupları ve Protokolü", ["Grup", "Önerilen Yaş Aralığı", "Aşılama Gerekçesi"], [
            {"cells": [{"text": "Rutin Hedef Grup", "isMasked": False}, {"text": "11-12 yaş kız ve erkekler", "isMasked": True, "hint": "ideal çocukluk dönemi"}, {"text": "Cinsel temas öncesi maksimum antikor yanıtı"}]},
            {"cells": [{"text": "Catch-up (Yakalama)", "isMasked": False}, {"text": "26 yaşına kadar genç bireyler", "isMasked": False}, {"text": "Kaçırılmış aşılamayı tamamlama ve koruma", "isMasked": True, "hint": "genç erişkinlikte telafi aşılaması"}]}
        ]),
        make_chain("Aşılama Yaş Basamakları", [
            "1. 11-12 Yaş Ziyareti: Çocuk rutin pediatrik aşı takviminde 2 doz HPV aşısına alınır.",
            "2. Yüksek Antikor Titresi: Genç yaşta erişkinin iki katı antikor titresi elde edilir.",
            "3. Gelecek Temas Koruması: Yıllar sonra cinsel aktif olunduğunda virüs doğrudan bloke edilir.",
            "4. 26 Yaşa Kadar Esneklik: Aşılanmamış üniversite gençliği aşılanarak riskten korunur."
        ]),
        make_recall("HPV aşılamasının rutin olarak önerildiği ideal yaş grubu ve catch-up (yakalama) üst yaş sınırı nedir?", "Rutin olarak 11-12 yaşındaki kız ve erkek çocuklara; catch-up olarak ise 26 yaşına kadar önerilir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: HPV Aşılama Yaş Grupları", [
            {"text": "Aşı rutin olarak 11-12 yaş kız ve erkek çocuklara önerilir.", "isLie": False, "explanation": "Doğru. Uluslararası standarttır."},
            {"text": "26 yaşına kadar genç kadın ve erkeklere catch-up yapılabilir.", "isLie": False, "explanation": "Doğru. 26 yaşa kadar önerilir."},
            {"text": "HPV aşısı sadece 95 yaş üzerindeki komadaki hastalara verilebilen bir aşıdır.", "isLie": True, "explanation": "Tuzak! Aşı 11-12 yaş çocuklara ve 26 yaşa kadar gençlere uygulanır."},
            {"text": "Cinsel temas öncesi yapılan aşının koruyuculuğu en yüksektir.", "isLie": False, "explanation": "Doğru. Viral karşılaşma öncesi esastır."}
        ]),
        make_quiz("HPV aşısının rutin olarak uygulanması önerilen standart hedef yaş grubu aşağıdakilerden hangisidir?", [
            {"key": "A", "text": "11-12 yaş kız ve erkek çocuklar", "isCorrect": True, "explanation": "Rutin takvim 11-12 yaş kız ve erkek çocukları hedefler."},
            {"key": "B", "text": "Yalnızca 60 yaş üzerindeki emekliler", "isCorrect": False, "explanation": "Geriatrik aşı değildir."},
            {"key": "C", "text": "Sadece 1 haftalık prematüre bebekler", "isCorrect": False, "explanation": "Prematüre yenidoğan aşısı değildir."},
            {"key": "D", "text": "Hiçbir yaş grubuna asla önerilmez", "isCorrect": False, "explanation": "DSÖ tarafından şiddetle önerilir."}
        ])
    ]
    slides.append(make_slide(55, "Aşı Hedef Yaş Grubu: 11-12 Yaş ve 26 Yaşa Kadar Yaklaşım", "Rutin hedef yaş, 11-12 yaş penceresi, cinsel temas öncesi bağışıklık ve 26 yaş catch-up", "Aşılama Yaş Protokolleri", s55_narrative, s55_bullets, s55_elements))

    # Slide 56: Erkek Aşılamasının Kritik Önemi ve Toplum Bağışıklığı
    s56_narrative = (
        "HPV aşılama programlarında erkek çocukların aşılanması, hem bireysel erkek sağlığı hem de "
        "toplum düzeyinde sürü bağışıklığı oluşturulması açısından yaşamsal öneme sahiptir.\n\n"
        "- **Bulaş Zincirini Kırma:** Erkekler asemptomatik taşıyıcı olarak HPV'nin kadınlara bulaşmasında "
        "en önemli rezervuarı oluşturur; erkeklerin aşılanması kadınları da dolaylı olarak korur.\n"
        "- **Erkeklerde HPV Maligniteleri:** HPV yalnızca serviks kanseri yapmaz; erkeklerde görülen "
        "**anal kanser, penis kanseri ve orofarenks (tonsil/dil kökü) kanserlerinin** de en önemli etkenidir.\n"
        "- **Kondilomların Önlenmesi:** Düşük riskli tipleri içeren aşılar erkeklerde anogenital siğilleri önler.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Erkek aşılaması hem bulaş zincirini kırarak toplum yükünü azaltır hem de erkeklerde anal ve orofaringeal kanser gelişimini önler."
    )
    s56_bullets = [
        "Erkekler kadınlara viral bulaşta en önemli rezervuardır.",
        "Erkek aşılaması toplum düzeyinde enfeksiyon yükünü azaltır.",
        "Erkeklerde anal kanser ve orofarenks kanserini önler."
    ]
    s56_elements = [
        make_cloze("Erkek aşılaması bulaş zincirini kırmanın yanında erkeklerde gelişebilecek anal kanser ve orofaringeal kanseri önler.", "anal kanser", "Erkeklerde HPV kaynaklı anogenital malignite"),
        make_table("Erkek Aşılamasının Temel Kazanımları", ["Kazanım Alanı", "Biyolojik Mekanizma", "Klinik / Epidemiyolojik Sonuç"], [
            {"cells": [{"text": "Bulaşın Engellenmesi", "isMasked": False}, {"text": "Erkek asemptomatik taşıyıcılığının kesilmesi", "isMasked": True, "hint": "taşıyıcı rezervuarın kurutulması"}, {"text": "Kadınlarda serviks kanserinde dolaylı azalma"}]},
            {"cells": [{"text": "Erkek Kanserleri", "isMasked": False}, {"text": "Onkojenik HPV maruziyetinin önlenmesi", "isMasked": False}, {"text": "Penis, anüs ve orofarenks kanserlerinden korunma", "isMasked": True, "hint": "erkek malignitelerine karşı bariyer"}]}
        ]),
        make_chain("Erkek Aşılamasından Sürü Bağışıklığına", [
            "1. Cinsiyetsiz Aşılama: 11-12 yaşta hem kız hem erkek çocuklar aşılanır.",
            "2. Viral Sirkülasyonun Durması: Popülasyonda virüsü aktaracak rezervuar kalmaz.",
            "3. Çift Yönlü Koruma: Kadında serviks, erkekte anal/orofaringeal kanser önlenir.",
            "4. Eliminasyon: Toplum düzeyinde HPV ilişkili tüm lezyonlar eradike olma yoluna girer."
        ]),
        make_recall("Erkek çocukların HPV'ye karşı aşılanmasının iki temel klinik ve epidemiyolojik gerekçesi nedir?", "Bulaş zincirini kırarak kadınları korumak ve erkeklerde görülen anal/orofaringeal kanserleri önlemektir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Erkek Aşılaması", [
            {"text": "Erkekler HPV'nin kadınlara bulaşmasında önemli rol oynar.", "isLie": False, "explanation": "Doğru. Majör bulaş rezervuarıdır."},
            {"text": "Erkek aşılaması anal kanser ve orofaringeal kanser sıklığını azaltır.", "isLie": False, "explanation": "Doğru. Erkek kanserlerine karşı korur."},
            {"text": "Erkeklere HPV aşısı yapıldığında erkeklerin boyu anında 4 metreye uzar.", "isLie": True, "explanation": "Tuzak! Aşı boy uzatmaz; bağışıklık sağlayarak kanser ve siğilleri önler."},
            {"text": "Toplum düzeyinde enfeksiyon yükünün kırılmasını sağlar.", "isLie": False, "explanation": "Doğru. Sürü bağışıklığı oluşturur."}
        ]),
        make_quiz("HPV aşılama programlarına erkek çocukların dahil edilmesinin temel gerekçesi aşağıdakilerden hangisidir?", [
            {"key": "A", "text": "Kadınlara bulaşı azaltmak ve erkeklerde anal/orofaringeal kanserleri önlemek", "isCorrect": True, "explanation": "Erkek aşılaması bulaş zincirini kırar ve erkek kanserlerini önler."},
            {"key": "B", "text": "Sadece erkeklerin askere gitmesini engellemek", "isCorrect": False, "explanation": "Askerlikle ilgisi yoktur."},
            {"key": "C", "text": "Yalnızca saç dökülmesini tedavi etmek", "isCorrect": False, "explanation": "Dermatolojik alopesi ilacı değildir."},
            {"key": "D", "text": "Erkeklerin spor müsabakalarında daha hızlı koşmasını sağlamak", "isCorrect": False, "explanation": "Doping maddesi değildir."}
        ])
    ]
    slides.append(make_slide(56, "Erkek Aşılamasının Kritik Önemi ve Toplum Bağışıklığı", "Bulaş zinciri, erkek rezervuarı, anal kanser, orofarenks kanseri ve sürü bağışıklığı", "Cinsiyetsiz Aşılama Stratejisi", s56_narrative, s56_bullets, s56_elements))

    # Slide 57: Aşı Tipleri: Dört Değerlikli ve Dokuz Değerlikli Aşılar
    s57_narrative = (
        "HPV aşıları kapsadıkları viral genotip sayısına göre iki değerlikli (bivalan), dört değerlikli "
        "(kuadrivalan) ve dokuz değerlikli (nonavalan) olmak üzere geliştirilmiştir.\n\n"
        "- **Dört Değerlikli Aşı (Gardasil):** En sık karşılaşılan **HPV 6, 11 (düşük risk)** ile "
        "**HPV 16, 18 (yüksek risk)** tiplerini içerir; hem kondilomlara hem de serviks kanserinin %70'ine karşı korur.\n"
        "- **Dokuz Değerlikli Aşı (Gardasil 9):** Bu 4 tipe ek olarak 5 ilave yüksek onkojenik genotipi "
        "**(HPV 31, 33, 45, 52 ve 58)** kapsar; serviks kanserlerine karşı koruma oranını **%90'ın üzerine** çıkarır.\n"
        "- **Koruma Süresi:** Aşıların sağladığı antikor korumasının **en az 10 yıl** sürdüğü kanıtlanmıştır "
        "ve bağışıklık hafızasının çok daha uzun ömürlü olduğu izlenmektedir.\n\n"
        "> [!NOTE]\n"
        "> Dokuz değerlikli aşı ek yüksek riskli tipleri kapsayarak kanser koruma oranını %90'ın üzerine taşır; koruma süresi en az 10 yıldır."
    )
    s57_bullets = [
        "Dört değerlikli aşı Tip 6, 11, 16 ve 18'i kapsar.",
        "Dokuz değerlikli aşı ek yüksek riskli 5 tipi (31, 33, 45, 52, 58) içerir.",
        "Aşının koruma süresi en az 10 yıldır."
    ]
    s57_elements = [
        make_cloze("Dokuz değerlikli HPV aşısı dört temel tipe ek olarak 31, 33, 45, 52 ve 58 tiplerini içerir.", "dokuz değerlikli", "Genişletilmiş yüksek riskli tipleri içeren aşı türü"),
        make_table("HPV Aşı Tipleri Karşılaştırması", ["Aşı Türü", "İçerdiği HPV Genotipleri", "Serviks Kanseri Koruma Oranı"], [
            {"cells": [{"text": "Dört Değerlikli", "isMasked": False}, {"text": "Tip 6, 11, 16, 18", "isMasked": True, "hint": "iki düşük ve iki yüksek riskli tip"}, {"text": "Yaklaşık %70 koruma"}]},
            {"cells": [{"text": "Dokuz Değerlikli", "isMasked": False}, {"text": "6, 11, 16, 18 + (31, 33, 45, 52, 58)", "isMasked": False}, {"text": "> %90 oranında genişletilmiş koruma", "isMasked": True, "hint": "maksimum kanser koruma gücü"}]}
        ]),
        make_chain("Aşı Gelişim Süreci", [
            "1. İlk Nesil: Tip 16 ve 18'e karşı bivalan/kuadrivalan aşılar geliştirildi.",
            "2. Genişletilmiş Nesil: 5 ek yüksek riskli tip eklenerek dokuz değerlikli form üretildi.",
            "3. Uzun Takip: Yapılan klinik çalışmalarla koruyuculuğun en az 10 yıl sürdüğü gösterildi.",
            "4. Küresel Etki: Popülasyon düzeyinde genital siğil ve CIN olguları çöktü."
        ]),
        make_recall("Dokuz değerlikli HPV aşısının dört değerlikli aşıya göre temel üstünlüğü nedir ve kanıtlanmış koruma süresi ne kadardır?", "Ek 5 yüksek riskli onkojenik tipi kapsayarak kanser korumasını %90'ın üzerine çıkarır; koruma süresi en az 10 yıldır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: HPV Aşı Tipleri", [
            {"text": "Dört değerlikli aşı tip 6, 11, 16 ve 18'i içerir.", "isLie": False, "explanation": "Doğru. Dörtlü formül budur."},
            {"text": "Dokuz değerlikli aşı ek yüksek riskli tipleri içerir.", "isLie": False, "explanation": "Doğru. Tip 31, 33, 45, 52, 58 eklenmiştir."},
            {"text": "HPV aşısı yapıldıktan 15 dakika sonra vücuttaki tüm antikorlar tamamen silinir.", "isLie": True, "explanation": "Tuzak! Koruma süresi en az 10 yıldır ve antikorlar uzun yıllar kanda kalır."},
            {"text": "Aşılar genital siğil ve serviks kanseri sıklığını belirgin azaltır.", "isLie": False, "explanation": "Doğru. Klinik başarısı kanıtlanmıştır."}
        ]),
        make_quiz("HPV aşılarının sağladığı kanıtlanmış koruyuculuk süresi en az ne kadardır?", [
            {"key": "A", "text": "En az 10 yıl", "isCorrect": True, "explanation": "Klinik takiplerde aşının en az 10 yıl güçlü koruma sağladığı kanıtlanmıştır."},
            {"key": "B", "text": "Sadece 3 gün", "isCorrect": False, "explanation": "Geçici koruma sağlamaz."},
            {"key": "C", "text": "Yalnızca 2 saat", "isCorrect": False, "explanation": "Aşılar uzun ömürlü immünite sağlar."},
            {"key": "D", "text": "Hiç koruma sağlamaz", "isCorrect": False, "explanation": "Yüksek koruma sağlar."}
        ])
    ]
    slides.append(make_slide(57, "Aşı Tipleri: Dört Değerlikli ve Dokuz Değerlikli Aşılar", "Kuadrivalan, nonavalan, genotip kapsayıcılığı, %90+ koruma ve en az 10 yıllık süre", "Aşı Tipleri ve Etkinlik", s57_narrative, s57_bullets, s57_elements))

    # Slide 58: Aşılama Sonrası Tarama Neden Bırakılamaz?
    s58_narrative = (
        "Toplumda en sık düşülen yanılgılardan biri, HPV aşısı olan bir kadının artık servikal kanser "
        "taramasına (Pap smear / HPV testi) ihtiyaç duymayacağı inancıdır; bu düşünce son derece tehlikelidir.\n\n"
        "- **1. Neden (Önceden Edinilmiş Enfeksiyon):** Aşı terapötik (tedavi edici) değildir; kadının "
        "aşı yapılmadan önce edinmiş olabileceği mevcut HPV enfeksiyonlarını veya lezyonları temizleyemez.\n"
        "- **2. Neden (Kapsanmayan Genotipler):** Dokuz değerlikli aşı dahi en sık görülen tipleri kapsar; "
        "serviks kanserine yol açabilen diğer nadir onkojenik HPV tipleri aşı kapsamında değildir.\n"
        "- **Altın Strateji Formülü:** Serviks kanseriyle mücadelede en kusursuz strateji: "
        "==Pap testi + HPV DNA testi + HPV aşılaması birlikteliğidir==.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] HPV aşıları servikal kanser taramasının yerine geçmez; aşılanan kadınlar rutin Pap ve HPV taramalarına aynı aralıklarla devam etmek zorundadır."
    )
    s58_bullets = [
        "HPV aşıları taramanın yerine geçmez; tarama devam etmelidir.",
        "Aşı önceden edinilmiş enfeksiyonları tedavi edemez.",
        "Aşı tüm onkojenik HPV tiplerini kapsamaz (strateji: Pap + HPV + Aşı)."
    ]
    s58_elements = [
        make_cloze("HPV aşıları mevcut enfeksiyonları temizlemediği ve tüm tipleri kapsamadığı için kanser taramasının yerine geçmez.", "taramasının", "Aşılamayla terk edilmemesi gereken rutin süreç"),
        make_table("Aşılı Kadında Taramanın Devam Etme Nedenleri", ["Gerekçe", "Biyolojik Gerçek", "Klinik Zorunluluk"], [
            {"cells": [{"text": "Mevcut Enfeksiyon", "isMasked": False}, {"text": "Aşı önceden var olan virüsü temizleyemez", "isMasked": True, "hint": "terapötik tedavi edici olmama"}, {"text": "Önceden başlamış displazi taranmalıdır"}]},
            {"cells": [{"text": "Aşı Dışı Tipler", "isMasked": False}, {"text": "Aşıda olmayan diğer nadir onkojenik tipler", "isMasked": False}, {"text": "Pap smear ile atipik hücre kontrolü şarttır", "isMasked": True, "hint": "nadir genotiplerin oluşturduğu risk"}]}
        ]),
        make_chain("Üçlü Koruma Stratejisi Zinciri", [
            "1. Aşılama: Çocuklukta primer koruma için VLP aşısı yapılır.",
            "2. Cinsel Yaşam: Yetişkinlikte aşının kapsamadığı nadir tiplerle temas olabilir.",
            "3. Rutin Ko-Test: 30 yaştan sonra düzenli Pap smear ve HPV DNA testi sürdürülür.",
            "4. Kusursuz Önleme: Üçlü strateji ile serviks kanseri gelişimi %100'e yakın engellenir."
        ]),
        make_recall("HPV aşısı olmuş bir kadının rutin servikal kanser tarama testlerini bırakamamasının iki temel nedeni nedir?", "Aşı öncesi edinilmiş enfeksiyonları tedavi edememesi ve aşının tüm onkojenik tipleri kapsamamasıdır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Aşılama ve Tarama Birlikteliği", [
            {"text": "HPV aşıları servikal kanser taramasının yerine geçmez.", "isLie": False, "explanation": "Doğru. Tarama aksatılmadan sürdürülür."},
            {"text": "Birçok kadın aşı öncesinde zaten enfekte olmuş olabilir.", "isLie": False, "explanation": "Doğru. Aşı tedavi edici değildir."},
            {"text": "Aşı olan bir kadın artık ömür boyu hiçbir jinekolojik muayeneye gitmemelidir.", "isLie": True, "explanation": "Tuzak! Aşılanan kadınlar da normal takvimle taranmaya devam etmelidir."},
            {"text": "Altın koruma formülü Pap testi, HPV testi ve aşılama birlikteliğidir.", "isLie": False, "explanation": "Doğru. En güçlü koruyucu sacayağıdır."}
        ]),
        make_quiz("HPV aşısı olan kadınlarda tarama programlarının (Pap smear / HPV testi) devam etmesi gerekliliğinin temel nedeni nedir?", [
            {"key": "A", "text": "Aşının önceki enfeksiyonları tedavi edememesi ve tüm onkojenik tipleri kapsamaması", "isCorrect": True, "explanation": "Aşı tedavi edici değildir ve tüm tipleri kapsamaz; bu yüzden tarama şarttır."},
            {"key": "B", "text": "Aşı yapılan kadınların derhal kör olması", "isCorrect": False, "explanation": "Böyle bir yan etki yoktur."},
            {"key": "C", "text": "Taramaların sadece aşı firmalarına para kazandırmak için yapılması", "isCorrect": False, "explanation": "Bilimsel tarama hayat kurtarır."},
            {"key": "D", "text": "Aşının hiçbir kadında antikor oluşturmaması", "isCorrect": False, "explanation": "Aşı mükemmel antikor üretir."}
        ])
    ]
    slides.append(make_slide(58, "Aşılama Sonrası Tarama Neden Bırakılamaz?", "Terapötik etkinlik yokluğu, aşı dışı genotipler, üçlü strateji (Pap + HPV + Aşı)", "Aşı Sonrası Tarama", s58_narrative, s58_bullets, s58_elements))

    # Slide 59: Üçlü Koruma Stratejisi: Pap + HPV Testi + Aşılama
    s59_narrative = (
        "Dünya Sağlık Örgütü ve jinekolojik onkoloji dernekleri, serviks kanserini yeryüzünden tamamen "
        "silmeyi (eliminasyon) hedefleyen kapsamlı bir koruyucu halk sağlığı sacayağı benimsemiştir.\n\n"
        "- **1. Ayak (Aşılama):** 11-12 yaş kız ve erkek çocukların aşılanması ile toplumdaki enfeksiyon "
        "rezervuarı kurutulur ve primer korunma sağlanır.\n"
        "- **2. Ayak (HPV DNA Testi):** 30 yaş ve üzerindeki kadınlarda yüksek duyarlılıkla persistan "
        "virüs taşıyıcıları yakalanır.\n"
        "- **3. Ayak (Pap Smear Sitolojisi):** Morfolojik displaziler ve sitolojik atipiler taranarak "
        "biyopsiye ve cerrahi küre yönlendirilir.\n"
        "- **Kolektif Güç:** Bu üç modalite birbirini dışlamaz; aksine bir arada uygulandığında serviks "
        "kanserini tamamen önlenebilir kılarlar.\n\n"
        "> [!NOTE]\n"
        "> Serviks kanserinin önlenmesindeki en etkin modern halk sağlığı stratejisi: Pap testi + HPV testi + aşılamadır."
    )
    s59_bullets = [
        "Modern onkoloji üçlü koruma sacayağını benimser.",
        "Aşılama primer, HPV testi etyolojik, Pap smear morfolojik koruma sağlar.",
        "Üç modalitenin birlikteliği kanseri neredeyse %100 önlenebilir kılar."
    ]
    s59_elements = [
        make_cloze("Serviks kanserinden korunmada en kusursuz yaklaşım Pap testi, HPV DNA testi ve aşılama birlikteliğidir.", "aşılama", "Üçlü koruma stratejisinin primer korunma basamağı"),
        make_table("Üçlü Koruma Stratejisinin Bileşenleri", ["Bileşen", "Koruma Düzeyi", "Temel İşlevi"], [
            {"cells": [{"text": "HPV Aşılaması", "isMasked": False}, {"text": "Primer (Birincil) Koruma", "isMasked": True, "hint": "enfeksiyon başlamadan engelleme"}, {"text": "Virüsün bulaşmasını ve yerleşmesini önleme"}]},
            {"cells": [{"text": "HPV DNA Testi", "isMasked": False}, {"text": "Moleküler İkincil Koruma", "isMasked": False}, {"text": "Yüksek riskli persistan virüsleri yakalama", "isMasked": True, "hint": "viral DNA varlığının tespiti"}]},
            {"cells": [{"text": "Pap Smear Sitolojisi", "isMasked": False}, {"text": "Morfolojik İkincil Koruma", "isMasked": False}, {"text": "Prekanseröz hücre atipilerini erken yakalama", "isMasked": True, "hint": "dökülen hücrelerde SIL tespiti"}]}
        ]),
        make_chain("Serviks Kanseri Eliminasyon Modeli", [
            "1. Aşılama Tabanı: Okul çağında kız ve erkek çocuklar yaygın aşılanır.",
            "2. Genç Erişkinlik: Maruziyet riski minimuma indirilmiş bir nesil yetişir.",
            "3. Erişkin Tarama: 30 yaş üstünde periyodik ko-test ile kaçaklar yakalanır.",
            "4. Sıfır Kanser: İnvaziv karsinom insidansı sıfıra yaklaşarak hastalık elenir."
        ]),
        make_recall("Modern jinekolojik onkolojide serviks kanserini önlemek için benimsenen üçlü koruma stratejisinin bileşenleri nelerdir?", "Pap smear sitolojisi + HPV DNA testi + HPV aşılamasıdır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Üçlü Koruma Stratejisi", [
            {"text": "Strateji Pap testi, HPV testi ve aşılama birlikteliğine dayanır.", "isLie": False, "explanation": "Doğru. Üçlü sacayağıdır."},
            {"text": "Aşı primer koruma, smear ve HPV testi ikincil koruma sağlar.", "isLie": False, "explanation": "Doğru. Koruma düzeyleri ayrımıdır."},
            {"text": "Üçlü stratejide hastaya günde beş kilo mangal kömürü yedirilmesi zorunludur.", "isLie": True, "explanation": "Tuzak! Tıbbi korumada aşılama, sitoloji ve moleküler testler yer alır; kömür tüketilmez."},
            {"text": "Birlikte uygulandığında kanseri önlemede maksimum başarı sağlanır.", "isLie": False, "explanation": "Doğru. Tamamlayıcı güç sunarlar."}
        ]),
        make_quiz("Serviks kanserinden korunmada en modern ve kusursuz halk sağlığı stratejisi hangi üç unsurun birlikteliğidir?", [
            {"key": "A", "text": "Pap testi + HPV DNA testi + HPV aşılaması", "isCorrect": True, "explanation": "Altın standart koruma sacayağı bu üç yöntemdir."},
            {"key": "B", "text": "Sadece aspirin + antibiyotik + antidepresan", "isCorrect": False, "explanation": "Kanser koruyucu strateji değildir."},
            {"key": "C", "text": "Yalnızca tuzlu su gargarası", "isCorrect": False, "explanation": "Faringeal basit yöntemdir."},
            {"key": "D", "text": "Hepsini bırakıp sadece şifalı taş takmak", "isCorrect": False, "explanation": "Bilim dışı yaklaşımdır."}
        ])
    ]
    slides.append(make_slide(59, "Üçlü Koruma Stratejisi: Pap + HPV Testi + Aşılama", "Primer ve sekonder koruma, moleküler tarama, eliminasyon hedefleri", "Koruyucu Halk Sağlığı", s59_narrative, s59_bullets, s59_elements))

    # Slide 60: [TEKRAR SAYFASI - CHECKPOINT 6] Moleküler Tarama ve HPV Aşılaması
    s60_narrative = (
        "Bölüm 6'da serviks karsinogenezini durduran modern moleküler tanı silahlarını (HPV DNA testi) "
        "ve primer korunmanın kilit unsuru olan aşı politikalarını eksiksiz pekiştirdik.\n\n"
        "- **HPV DNA Testi:** Yüksek riskli genotipleri saptamada son derece hassastır; **özellikle 30 yaş ve "
        "üzerinde** değerlidir. Negatif test sonucu izleyen **5 yıl boyunca neoplazi riskinin çok düşük** olduğunu gösterir.\n"
        "- **Aşılama İlkeleri:** L1 kapsid proteininden oluşan VLP teknolojisine dayanır; viral DNA içermez. "
        "Rutin olarak **11-12 yaş kız ve erkek çocuklara**; catch-up olarak **26 yaşa kadar** gençlere önerilir.\n"
        "- **Erkeklerin Rolü:** Erkek aşılaması hem kadınlara bulaş zincirini kırar hem de erkeklerde **anal ve "
        "orofarenks kanserlerini** önler.\n"
        "- **Üçlü Sacayağı:** Aşı taramanın yerine geçmez; en kusursuz strateji **Pap + HPV + Aşı** birlikteliğidir.\n\n"
        "> [!IMPORTANT]\n"
        "> [BÖLÜM 6 SENTEZİ] HPV testi 30 yaş üstünde değerlidir ve 5 yıllık güvence verir; aşılama 11-12 yaşta cinsiyetsiz yapılır ve en az 10 yıl korur; aşılı kadınlar da rutin taramaya devam etmek zorundadır."
    )
    s60_bullets = [
        "HPV DNA testi ≥30 yaşta değerlidir; negatifliği 5 yıllık koruyucu güvence sağlar.",
        "Aşı 11-12 yaş kız ve erkeklere önerilir, VLP yapısındadır, en az 10 yıl korur.",
        "Erkek aşılaması bulaşı keser, anal ve orofarenks kanserini önler.",
        "Aşı taramayı sonlandırmaz; formül Pap + HPV testi + aşılamadır."
    ]
    s60_elements = [
        make_cloze("Bölüm 6 sentezinde pekiştirilen HPV aşılamasının rutin hedef kitlesi 11-12 yaş çocuklardır.", "11-12 yaş", "Bölüm 6 checkpointinde yinelenen ideal aşılama yaşı"),
        make_table("Bölüm 6 Tarama ve Korunma Sentez Tablosu", ["Uygulama / Yöntem", "Temel Hedef Kitle / Değer", "Klinik / Halk Sağlığı Anlamı"], [
            {"cells": [{"text": "HPV DNA Testi", "isMasked": False}, {"text": "≥30 yaş kadınlar (5 yıl güvence)", "isMasked": True, "hint": "erişkin tarama yaşı ve koruma penceresi"}, {"text": "Persistan onkojenik enfeksiyon tespiti"}]},
            {"cells": [{"text": "HPV Aşılaması", "isMasked": False}, {"text": "11-12 yaş kız ve erkekler", "isMasked": False}, {"text": "Primer korunma ve en az 10 yıl koruyuculuk", "isMasked": True, "hint": "uzun ömürlü antikor koruması"}]},
            {"cells": [{"text": "Üçlü Strateji", "isMasked": False}, {"text": "Pap + HPV testi + Aşılama", "isMasked": False}, {"text": "Kanseri yeryüzünden silme formülü", "isMasked": True, "hint": "kapsamlı koruyucu yaklaşım"}]}
        ]),
        make_chain("Bölüm 6 Koruma Entegrasyonu", [
            "1. Aşılama: 11-12 yaşında kız ve erkek çocuk aşılanarak nötralizan antikor üretilir.",
            "2. Moleküler Güvenlik: 30 yaşından sonra 5 yılda bir HPV DNA testi ile kontrol yapılır.",
            "3. Negatiflik Konforu: HPV negatifse sonraki 5 yıl boyunca kadın neoplaziden korunur.",
            "4. Tam Koruma: Aşı ve tarama el ele vererek invaziv karsinomu imkansız kılar."
        ]),
        make_recall("Bölüm 6'da öğrendiğimiz: (1) HPV DNA testinin en değerli olduğu yaş, (2) Aşının rutin yaşı ve (3) Aşının kanıtlanmış minimum koruma süresi nedir?", "(1) ≥30 yaş, (2) 11-12 yaş kız ve erkekler, (3) En az 10 yıldır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Bölüm 6 Checkpoint Sentezi", [
            {"text": "HPV DNA testi özellikle 30 yaş ve üzeri kadınlarda değerlidir.", "isLie": False, "explanation": "Doğru. Persistan enfeksiyonu gösterir."},
            {"text": "HPV aşıları rutin olarak 11-12 yaş kız ve erkek çocuklara önerilir.", "isLie": False, "explanation": "Doğru. Standart aşılama takvimidir."},
            {"text": "Aşılanan bir kadında serviks kanseri taraması derhal ömür boyu yasaklanmalıdır.", "isLie": True, "explanation": "Tuzak! Aşı taramanın yerine geçmez; aşılanan kadınlar da rutin taramaya devam etmelidir."},
            {"text": "Aşıların sağladığı koruma süresi en az 10 yıldır.", "isLie": False, "explanation": "Doğru. Klinik verilerle kanıtlanmıştır."}
        ]),
        make_quiz("Bölüm 6'da pekiştirilen moleküler tarama ve aşılama ilkelerine göre aşağıdakilerden hangisi YANLIŞTIR?", [
            {"key": "A", "text": "HPV aşısı olan kadınların bir daha asla Pap smear yaptırmasına gerek yoktur", "isCorrect": True, "explanation": "Yanlış önerme! Aşı tüm tipleri kapsamadığı ve eskiyi silmediği için tarama zorunludur."},
            {"key": "B", "text": "Yüksek riskli HPV negatifliği 5 yıllık güvenli pencere sağlar", "isCorrect": False, "explanation": "Doğru bilgidir."},
            {"key": "C", "text": "Erkek aşılaması anal ve orofaringeal kanserleri önler", "isCorrect": False, "explanation": "Doğru bilgidir."},
            {"key": "D", "text": "Dokuz değerlikli aşı kansere karşı %90'ın üzerinde koruma sağlar", "isCorrect": False, "explanation": "Doğru bilgidir."}
        ])
    ]
    slides.append(make_slide(60, "[TEKRAR SAYFASI - CHECKPOINT 6] Moleküler Tarama ve HPV Aşılaması", "Bölüm 6 kapsamlı tekrarı: HPV testi, 5 yıl güvencesi, aşı takvimi ve üçlü koruma modeli", "Bölüm Tekrarı ve Konsolidasyon", s60_narrative, s60_bullets, s60_elements))

    return slides

if __name__ == '__main__':
    slides = get_sec6()
    print(f"Sec6 generated: {len(slides)} slides (Slide 51 to 60)")
    for s in slides:
        print(f" - Slide {s['slideNumber']}: {s['title']} ({len(s['interactiveElements'])} elements, {len(s['content'].split())} words)")
