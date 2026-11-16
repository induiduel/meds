import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from meds.scripts.deck_generators.builder_helper import make_slide, make_cloze, make_table, make_chain, make_recall, make_spot_lie, make_quiz

def get_sec5():
    slides = []

    # Slide 41: SIL Yaş Dağılımı ve Zirve Yaşları
    s41_narrative = (
        "Servikal intraepitelyal neoplazilerin ve invaziv serviks karsinomunun yaş dağılım eğrileri, "
        "hastalığın karsinogenez basamaklarının zaman çizelgesini net olarak ortaya koyar.\n\n"
        "- **SIL İnsidans Zirvesi:** Skuamöz intraepitelyal lezyonların (özellikle HSIL) toplumdaki "
        "görülme sıklığı **yaklaşık 30 yaş civarında zirve** yapar.\n"
        "- **Karsinom İnsidans Zirvesi:** İnvaziv karsinom ise bu preinvaziv lezyon pikinden **10 ila 15 yıl sonra**, "
        "ortalama **yaklaşık 45 yaş civarında** zirveye ulaşır.\n"
        "- **Latent Dönem ve Tarama Fırsatı:** SIL piki ile karsinom piki arasındaki bu 10-15 yıllık geniş zaman penceresi, "
        "tarama programları (Pap smear ve HPV DNA) ile kanserin henüz invazyon yapmadan yakalanması için eşsiz bir klinik fırsat sunar.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] SIL insidansı yaklaşık 30 yaşta zirve yaparken; invaziv karsinom bundan 10-15 yıl sonra yaklaşık 45 yaş civarında zirve yapar."
    )
    s41_bullets = [
        "SIL insidansı ~30 yaş civarında zirve yapar.",
        "İnvaziv karsinom insidansı ~45 yaş civarında zirve yapar.",
        "İki zirve arasındaki 10-15 yıllık latent pencere tarama fırsatıdır."
    ]
    s41_elements = [
        make_cloze("SIL insidansı yaklaşık 30 yaş civarında zirve yaparken invaziv karsinom yaklaşık 45 yaş civarında zirve yapar.", "30 yaş", "SIL insidansının pik yaptığı yaş"),
        make_table("SIL ve İnvaziv Karsinom Yaş Dinamikleri", ["Hastalık Evresi", "Zirve Yaşı (Pik)", "Patolojik Durum"], [
            {"cells": [{"text": "Prekanseröz SIL", "isMasked": False}, {"text": "Yaklaşık 30 yaş", "isMasked": True, "hint": "üreme çağının üçüncü dekadı"}, {"text": "İntraepitelyal displazi ve hücresel atipi"}]},
            {"cells": [{"text": "İnvaziv Karsinom", "isMasked": False}, {"text": "Yaklaşık 45 yaş", "isMasked": False}, {"text": "Stromal invazyon ve stromal desmoplazi", "isMasked": True, "hint": "bazal membranın aşılması"}]}
        ]),
        make_chain("Zaman İçinde Karsinogenez Kronolojisi", [
            "1. Cinsel Aktivite Başı: 18-22 yaşta ilk HPV enfeksiyonu edinilir.",
            "2. SIL Zirvesi: 30 yaş civarında lezyonlar HSIL/CIN evresinde pik yapar.",
            "3. Latent Dönem: 10-15 yıl boyunca hücresel genetik mutasyonlar birikir.",
            "4. Karsinom Zirvesi: 45 yaş civarında bazal membran delinerek invaziv kanser zirveye ulaşır."
        ]),
        make_recall("SIL insidansı ile invaziv karsinom insidansının pik yaptığı yaşlar nelerdir ve aralarındaki fark ne kadardır?", "SIL ~30 yaşta, invaziv karsinom ~45 yaşta zirve yapar; aralarında yaklaşık 10-15 yıllık bir süre vardır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: SIL ve Karsinom Yaş Dağılımı", [
            {"text": "SIL insidansı yaklaşık 30 yaş civarında zirve yapar.", "isLie": False, "explanation": "Doğru. Genç erişkinlikte pik yapar."},
            {"text": "İnvaziv karsinom insidansı yaklaşık 45 yaş civarında zirve yapar.", "isLie": False, "explanation": "Doğru. SIL'den 10-15 yıl sonra pik yapar."},
            {"text": "İnvaziv serviks kanseri daima yeni doğmuş bebeklerde ilk 2 saatte zirve yapar.", "isLie": True, "explanation": "Tuzak! Serviks kanseri yenidoğan hastalığı değildir; ortalama 45 yaş civarında zirveye ulaşır."},
            {"text": "İki pik arasındaki 10-15 yıllık latent süre tarama için ideal bir fırsattır.", "isLie": False, "explanation": "Doğru. Erken yakalama bu aralıkta yapılır."}
        ]),
        make_quiz("Skuamöz intraepitelyal lezyon (SIL) insidansının toplumda zirve yaptığı ortalama yaş kaçtır?", [
            {"key": "A", "text": "Yaklaşık 30 yaş", "isCorrect": True, "explanation": "SIL insidansı ~30 yaşta pik yapar."},
            {"key": "B", "text": "Yaklaşık 85 yaş", "isCorrect": False, "explanation": "SIL genç kadınlarda pik yapar."},
            {"key": "C", "text": "Henüz anne karnında 3 aylıkken", "isCorrect": False, "explanation": "Embriyonik dönemde görülmez."},
            {"key": "D", "text": "Sadece 100 yaş üzerindeki asırlık bireylerde", "isCorrect": False, "explanation": "Geriatrik pik değildir."}
        ])
    ]
    slides.append(make_slide(41, "SIL Yaş Dağılımı ve Zirve Yaşları", "SIL piki (~30 yaş), invaziv karsinom piki (~45 yaş), 10-15 yıllık latent pencere", "Epidemiyoloji ve Yaş Dinamikleri", s41_narrative, s41_bullets, s41_elements))

    # Slide 42: SIL Klinik Seyri ve Semptomsuz Doğası
    s42_narrative = (
        "Skuamöz intraepitelyal lezyonların (hem LSIL hem de HSIL) klinik pratikteki en tehlikeli yönü, "
        "hastada belirgin hiçbir şikayet yaratmaksızın **tamamen asemptomatik** seyretmeleridir.\n\n"
        "- **Semptom Yokluğu:** Displazi epitel katmanlarıyla sınırlı kaldığından, sinir uçlarını veya damarları "
        "istila etmez; bu nedenle ağrı, kaşıntı veya belirgin kanama yapmaz.\n"
        "- **Rutin Taramada Yakalanma:** Hastaların neredeyse tamamı rutin jinekolojik kontrol veya rutin "
        "**Pap smear taraması** sırasında tesadüfen saptanır.\n"
        "- **Klinik Farkındalık:** Hastanın kendini tamamen sağlıklı hissetmesi tarama programlarının "
        "toplum bazında aksatılmadan yürütülmesinin ne kadar hayati olduğunu gösterir.\n\n"
        "> [!NOTE]\n"
        "> SIL lezyonları genellikle asemptomatiktir; tanı klinik şikayetle değil, tarama programları ile konur."
    )
    s42_bullets = [
        "SIL lezyonları genellikle tamamen asemptomatiktir.",
        "Ağrı, kaşıntı veya belirgin akıntı oluşturmaz.",
        "Tanı rutin Pap smear taramalarında şans eseri yakalanır."
    ]
    s42_elements = [
        make_cloze("SIL lezyonları sinir ve damar invazyonu yapmadığından genellikle asemptomatik olarak seyreder.", "asemptomatik", "Belirti ve şikayet vermeyen klinik seyir biçimi"),
        make_table("SIL Klinik Prezentasyon Özellikleri", ["Klinik Parametre", "Gözlenen Durum", "Klinik Yansıması"], [
            {"cells": [{"text": "Ağrı / Acı", "isMasked": False}, {"text": "Kesinlikle yoktur", "isMasked": True, "hint": "semptomsuz seyir"}, {"text": "Hasta doktora gitme gereği duymaz"}]},
            {"cells": [{"text": "Tanı Zamanı", "isMasked": False}, {"text": "Rutin tarama smeari", "isMasked": False}, {"text": "Erken displazi evresinde yakalanır", "isMasked": True, "hint": "preinvaziv dönemde tespit"}]}
        ]),
        make_chain("Sessiz Seyirden Taramayla Tanıya", [
            "1. İntraepitelyal Büyüme: Displastik hücreler epitel içinde sessizce çoğalır.",
            "2. Klinik Sessizlik: Damar ve sinir tutulmadığı için hiçbir semptom oluşmaz.",
            "3. Rutin Sağlık Kontrolü: Hasta şikayetsiz halde Pap smear taramasına girer.",
            "4. Sitolojik Uyarı: Mikroskopta atipik hücreler görülerek ileri tetkike yönlendirilir."
        ]),
        make_recall("SIL lezyonlarının kliniğe başvuru semptomları nasıldır ve hastalar lezyonlarından nasıl haberdar olur?", "Genellikle tamamen asemptomatiktir; hastalar rutin tarama testleri (Pap smear) sırasında tanı alır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: SIL Klinik Prezentasyonu", [
            {"text": "SIL lezyonları genellikle asemptomatik seyreder.", "isLie": False, "explanation": "Doğru. Belirti vermezler."},
            {"text": "Displaziler ağrı veya ateş oluşturmaz.", "isLie": False, "explanation": "Doğru. Sinsi ve sessizdir."},
            {"text": "SIL hastalarında ilk günden itibaren tüm vücutta deriyi patlatan şimşek ağrıları olur.", "isLie": True, "explanation": "Tuzak! SIL tamamen asemptomatiktir; hiçbir ağrı veya şikayet yapmaz."},
            {"text": "Tanı çoğunlukla rutin Pap testleri ile konur.", "isLie": False, "explanation": "Doğru. Taramayla yakalanır."}
        ]),
        make_quiz("Servikal intraepitelyal lezyonların (SIL) tipik klinik prezentasyonu aşağıdakilerden hangisidir?", [
            {"key": "A", "text": "Genellikle tamamen asemptomatiktir ve rutin taramada saptanır", "isCorrect": True, "explanation": "SIL lezyonları genellikle belirti vermez ve taramayla yakalanır."},
            {"key": "B", "text": "Yüksek ateş ve generalize konvülsiyon krizleri", "isCorrect": False, "explanation": "Nörolojik veya sistemik belirti vermez."},
            {"key": "C", "text": "Masif gastrointestinal kanama", "isCorrect": False, "explanation": "Sindirim sistemiyle ilgisi yoktur."},
            {"key": "D", "text": "Ani başlayan bilateral körlük", "isCorrect": False, "explanation": "Görme sistemiyle ilgisi yoktur."}
        ])
    ]
    slides.append(make_slide(42, "SIL Klinik Seyri ve Semptomsuz Doğası", "Asemptomatik gidişat, sinir/damar tutulumu yokluğu ve taramanın hayati rolü", "Klinik Özellikler", s42_narrative, s42_bullets, s42_elements))

    # Slide 43: Tanısal Basamaklar: Pap Testinden Kolposkopiye
    s43_narrative = (
        "Servikal neoplazilerin erken tanısında basamaklı bir tanısal algoritma uygulanır. Süreç popülasyon "
        "taraması ile başlar ve doku doğrulaması ile sonlanır.\n\n"
        "- **1. Basamak (Sitolojik Tarama):** Asemptomatik kadında yapılan rutin **Pap smear testi** ile "
        "anormal displastik hücrelerin varlığı taranır.\n"
        "- **2. Basamak (Görsel Büyütme):** Smearinde anormal sitoloji (ASCUS, LSIL, HSIL) saptanan hastalara "
        "serviksin büyütülerek incelendiği **kolposkopi** uygulanır.\n"
        "- **3. Basamak (Biyopsi):** Kolposkopik muayenede şüpheli alanlar belirlenerek hedef biyopsi alınır; "
        "kesin tanı histopatolojik inceleme ile konur.\n\n"
        "> [!NOTE]\n"
        "> Tanı süreci basamaklıdır: Anormal Pap testi → Kolposkopik muayene → Hedefe yönelik biyopsi."
    )
    s43_bullets = [
        "Süreç anormal Pap smear sonucuyla başlar.",
        "İkinci aşama kolposkopi ile serviksin incelenmesidir.",
        "Kesin tanı şüpheli odaktan alınan biyopsinin histopatolojisiyle konur."
    ]
    s43_elements = [
        make_cloze("Anormal sitoloji saptanan hastada serviksin büyütülerek incelenmesini sağlayan optik yönteme kolposkopi adı verilir.", "kolposkopi", "Serviksi mikroskop benzeri optik lenslerle inceleme"),
        make_table("Servikal Tanısal Basamaklar", ["Basamak", "Kullanılan Yöntem", "Temel İşlev"], [
            {"cells": [{"text": "Tarama Basamağı", "isMasked": False}, {"text": "Pap smear ve HPV testi", "isMasked": True, "hint": "hücresel ve viral tarama"}, {"text": "Riskli hastaların tespiti"}]},
            {"cells": [{"text": "Doğrulama Basamağı", "isMasked": False}, {"text": "Kolposkopi altında punch biyopsi", "isMasked": False}, {"text": "Histopatolojik kesin tanı (CIN evresi)", "isMasked": True, "hint": "doku tanısı ve derecelendirme"}]}
        ]),
        make_chain("Tanısal Algoritma Akışı", [
            "1. Smear Sonucu: Rutin Pap testinde anormal epitelyal lezyon (SIL) rapor edilir.",
            "2. Kolposkopi Randevusu: Hasta jinekoloji polikliniğinde optik büyütmeye alınır.",
            "3. Hedef Alan Tespiti: Anormal epitel sınırları belirlenerek doku forsepsiyle örneklenir.",
            "4. Patoloji Raporu: Biyopsi sonucu CIN derecesine göre tedavi haritasını çizer."
        ]),
        make_recall("Anormal Pap smear sonucu gelen bir hastada izlenmesi gereken tanısal takip basamakları nelerdir?", "Hasta kolposkopiye yönlendirilir, şüpheli alanlar incelenir ve biyopsi alınarak histolojik tanı konur."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Tanısal Basamaklar", [
            {"text": "Tanı akışı anormal Pap testi ile başlar.", "isLie": False, "explanation": "Doğru. Tarama başlangıç noktasıdır."},
            {"text": "İkinci basamakta kolposkopik değerlendirme yapılır.", "isLie": False, "explanation": "Doğru. Serviks optik olarak büyütülür."},
            {"text": "Smearinde şüphe çıkan her hastaya biyopsi yapmadan hemen açık kalp ameliyatı uygulanır.", "isLie": True, "explanation": "Tuzak! Kalp ameliyatı değil, servikse kolposkopik inceleme ve biyopsi yapılır."},
            {"text": "Kesin tanı doku biyopsisinin histopatolojik incelemesiyle konur.", "isLie": False, "explanation": "Doğru. Altın standart biyopsidir."}
        ]),
        make_quiz("Anormal Pap smear sitolojisi rapor edilen bir hastada atılacak bir sonraki standart tanı basamağı nedir?", [
            {"key": "A", "text": "Kolposkopik inceleme ve şüpheli alanlardan biyopsi yapılması", "isCorrect": True, "explanation": "Anormal sitolojide sonraki adım kolposkopi ve biyopsidir."},
            {"key": "B", "text": "Hastanın derhal karantina koğuşuna kapatılması", "isCorrect": False, "explanation": "Karantina gerektiren bir enfeksiyon değildir."},
            {"key": "C", "text": "Tüm dişlerin cerrahi olarak çekilmesi", "isCorrect": False, "explanation": "Diş hekimliği ile ilgisi yoktur."},
            {"key": "D", "text": "Hiçbir şey yapmadan 40 yıl beklenmesi", "isCorrect": False, "explanation": "Takip ve doğrulama zorunludur."}
        ])
    ]
    slides.append(make_slide(43, "Tanısal Basamaklar: Pap Testinden Kolposkopiye", "Tarama sitolojisi, optik büyütme, yönlendirilmiş biyopsi ve tanısal zincir", "Tanısal Algoritma", s43_narrative, s43_bullets, s43_elements))

    # Slide 44: Kolposkopi ve Asetik Asit: Asetobeyaz Epitel
    s44_narrative = (
        "Kolposkopi, serviks yüzeyinin özel bir aydınlatma ve optik büyütme sistemiyle doğrudan görsel "
        "olarak incelendiği girişimsel olmayan muayene yöntemidir.\n\n"
        "- **Asetik Asit Uygulaması:** İnceleme sırasında servikal mukozaya pamuk yardımıyla **%3 ila %5'lik "
        "seyreltik asetik asit (sirke ruhu)** solüsyonu uygulanır.\n"
        "- **Asetobeyaz Reaksiyon Mekanizması:** Asetik asit, displastik hücrelerde aşırı miktarda artmış olan "
        "**nükleer proteinleri geçici olarak pıhtılaştırır (koagüle eder)**; ışık bu katılaşmış proteinlerden "
        "yansıyarak lezyonlu alanın **opak tebeşir beyazı (asetobeyaz)** renkte parlamasına yol açar.\n"
        "- **Biyopsi Hedefleme:** Normal epitel pembe kalırken, asetobeyaz alanlar kolposkopiste tam olarak "
        "nereden punch biyopsi alması gerektiğini gösterir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Kolposkopide lezyonlar asetik asit uygulanmasıyla vurgulanır; artmış nükleer proteinlerin çökelmesi asetobeyaz epitel reaksiyonunu oluşturur."
    )
    s44_bullets = [
        "Servikse %3-5'lik asetik asit solüsyonu uygulanır.",
        "Displastik alanlardaki artmış nükleer proteinler çökelerek beyazlaşır.",
        "Oluşan asetobeyaz epitel biyopsi alınacak hedefi gösterir."
    ]
    s44_elements = [
        make_cloze("Kolposkopi sırasında displastik alanların beyaz görünmesini sağlayan reaksiyona asetobeyaz epitel reaksiyonu adı verilir.", "asetobeyaz", "Asetik asit ile beyazlaşan patolojik alan"),
        make_table("Kolposkopik Reaksiyon Dinamikleri", ["Solüsyon", "Hücresel Hedef", "Gözlenen Renk Değişimi"], [
            {"cells": [{"text": "Asetik Asit (%3-5)", "isMasked": False}, {"text": "Çekirdekteki yoğun nükleer proteinler", "isMasked": True, "hint": "atipik nükleus protein yükü"}, {"text": "Opak asetobeyaz reaksiyon"}]},
            {"cells": [{"text": "Normal Epitel Yanıtı", "isMasked": False}, {"text": "Düşük nükleus/sitoplazma oranı", "isMasked": False}, {"text": "Pembe, yarı saydam ve homojen kalır", "isMasked": True, "hint": "normal mukoza görünümü"}]}
        ]),
        make_chain("Asetobeyaz Reaksiyon Mekanizması", [
            "1. Solüsyon Teması: Servikal yüzeye %3-5 asetik asit uygulanır.",
            "2. Protein Koagülasyonu: Yüksek nükleuslu atipik hücrelerde nükleer proteinler pıhtılaşır.",
            "3. Işık Yansıması: Epitelin saydamlığı kaybolur ve ışık geçirgenliği engellenir.",
            "4. Beyazlaşma: Kolposkopi altında keskin sınırlı beyaz lezyon belirir ve biyopsi alınır."
        ]),
        make_recall("Kolposkopide displastik servikal alanları görünür kılmak için hangi kimyasal madde kullanılır ve lezyonlar nasıl görünür?", "Asetik asit (%3-5) kullanılır; displastik alanlar asetobeyaz (opak beyaz) reaksiyon verir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Kolposkopi ve Asetobeyaz Epitel", [
            {"text": "Kolposkopide lezyonlar asetik asit uygulanması ile vurgulanır.", "isLie": False, "explanation": "Doğru. Asetik asit standart solüsyondur."},
            {"text": "Nükleer proteinlerin çökelmesi sonucu doku beyaz renkte izlenir.", "isLie": False, "explanation": "Doğru. Asetobeyaz reaksiyon mekanizmasıdır."},
            {"text": "Kolposkopide kullanılan asetik asit tüm rahmi eritip vajinadan akıtan saf hidroklorik asittir.", "isLie": True, "explanation": "Tuzak! Kullanılan madde seyreltik %3-5 asetik asittir; dokuyu eritmez, geçici opaklık verir."},
            {"text": "Asetobeyaz alanlar hedefe yönelik biyopsi alınmasını sağlar.", "isLie": False, "explanation": "Doğru. Kolposkopik haritalama sağlar."}
        ]),
        make_quiz("Kolposkopik muayenede servikal intraepitelyal lezyonların belirginleşmesini sağlayan kimyasal solüsyon nedir?", [
            {"key": "A", "text": "Asetik asit solüsyonu", "isCorrect": True, "explanation": "Asetik asit lezyonları asetobeyaz renge dönüştürerek vurgular."},
            {"key": "B", "text": "Konsantre sülfürik asit", "isCorrect": False, "explanation": "Doku yıkımı yapar, kullanılmaz."},
            {"key": "C", "text": "Saf zeytinyağı", "isCorrect": False, "explanation": "Optik kontrast sağlamaz."},
            {"key": "D", "text": "Sodyum bikarbonat şurubu", "isCorrect": False, "explanation": "Protein çökeltme yapmaz."}
        ])
    ]
    slides.append(make_slide(44, "Kolposkopi ve Asetik Asit: Asetobeyaz Epitel", "Asetik asit uygulaması, nükleer protein koagülasyonu, asetobeyaz epitel ve biyopsi", "Kolposkopik Bulgular", s44_narrative, s44_bullets, s44_elements))

    # Slide 45: LSIL ve HSIL Klinik Yönetim Prensipleri
    s45_narrative = (
        "Biyopsi ile doğrulanmış preinvaziv servikal lezyonların klinik yönetimi, lezyonun derecesine "
        "ve hastanın taşıdığı kanserleşme riskine göre katı algoritmalara bağlanmıştır.\n\n"
        "- **LSIL (CIN I) Yönetimi:** Doğal seyrinde yüksek oranda kendiliğinden gerileme eğilimi olduğundan, "
        "biyopsiyle doğrulanmış genç hastalarda **konservatif yaklaşım ve yakın takip** (aralıklı Pap/HPV testi) esastır; "
        "agresif cerrahiden kaçınılır.\n"
        "- **HSIL (CIN II-III) Yönetimi:** Yüksek malign transformasyon riski nedeniyle agresif yaklaşım şarttır; "
        "standart tedavi **cerrahi eksizyondur (LEEP veya konik biyopsi / konizasyon)**.\n"
        "- **Kalıcı LSIL Durumu:** Takipte 2 yıldan uzun süre gerilemeyen kalıcı LSIL olgularında da eksizyonel cerrahi gündeme gelir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Biyopsi ile doğrulanmış LSIL'de yakın takip ve konservatif yaklaşım esasken; HSIL veya kalıcı LSIL olgularında cerrahi eksizyon (konik biyopsi / LEEP) uygulanır."
    )
    s45_bullets = [
        "Doğrulanmış LSIL'de yakın takip ve konservatif yaklaşım esastır.",
        "HSIL veya kalıcı LSIL varlığında cerrahi eksizyon (konik biyopsi) uygulanır.",
        "Tedavi seçimi malign transformasyon riskine göre belirlenir."
    ]
    s45_elements = [
        make_cloze("HSIL veya kalıcı LSIL varlığında lezyonun çıkarılmasını sağlayan cerrahi işleme konik biyopsi adı verilir.", "konik biyopsi", "Transformasyon zonunun koni şeklinde cerrahi çıkarılması"),
        make_table("SIL Klinik Yönetim Protokolü", ["Lezyon Derecesi", "Primer Tedavi Yaklaşımı", "Tedavi Gerekçesi"], [
            {"cells": [{"text": "Biyopsiyle Doğrulanmış LSIL", "isMasked": False}, {"text": "Konservatif izlem ve yakın takip", "isMasked": True, "hint": "cerrahisiz bekleme ve izlem"}, {"text": "Yüksek spontan regresyon oranı (%60)"}]},
            {"cells": [{"text": "HSIL (CIN II-III)", "isMasked": False}, {"text": "Cerrahi eksizyon (LEEP / Konizasyon)", "isMasked": False}, {"text": "İnvaziv karsinoma ilerleme riski", "isMasked": True, "hint": "kanserleşme tehlikesini önleme"}]}
        ]),
        make_chain("Yönetim Karar Algoritması", [
            "1. Biyopsi Raporu: Patoloji CIN derecesini (I, II veya III) kesinleştirir.",
            "2. CIN I Yolu: Doğurganlık korunur, 6-12 ay sonra smear ve kolposkopi tekrarlanır.",
            "3. CIN II/III Yolu: LEEP veya soğuk konizasyon ile transformasyon zonu çıkarılır.",
            "4. Cerrahi Sınır Kontrolü: Çıkarılan koninin cerrahi sınırlarında lezyonun temiz olduğu doğrulanır."
        ]),
        make_recall("Biyopsi ile doğrulanmış LSIL ile HSIL lezyonlarının standart klinik yönetimleri arasındaki temel fark nedir?", "LSIL'de yakın takip ve konservatif yaklaşım uygulanırken; HSIL'de cerrahi eksizyon (konik biyopsi / LEEP) yapılır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: SIL Klinik Yönetimi", [
            {"text": "Biyopsi ile doğrulanmış LSIL'de yakın takip ve konservatif yaklaşım esastır.", "isLie": False, "explanation": "Doğru. Gereksiz cerrahi yapılmaz."},
            {"text": "HSIL veya kalıcı LSIL cerrahi eksizyon (konik biyopsi) ile tedavi edilir.", "isLie": False, "explanation": "Doğru. Eksizyon standarttır."},
            {"text": "CIN I saptanan tüm kadınlara acil kemik iliği nakli ve radyasyon banyosu verilir.", "isLie": True, "explanation": "Tuzak! CIN I selim bir tablodur, nakil veya radyasyon verilmez; yalnızca izlenir."},
            {"text": "Cerrahi tedavide LEEP veya konizasyon sık kullanılan yöntemlerdir.", "isLie": False, "explanation": "Doğru. Eksizyonel yöntemlerdir."}
        ]),
        make_quiz("Biyopsi ile doğrulanmış HSIL (CIN II-III) olgusunda standart klinik tedavi yaklaşımı nedir?", [
            {"key": "A", "text": "Cerrahi eksizyon (konik biyopsi veya LEEP)", "isCorrect": True, "explanation": "HSIL tedavisinde eksizyonel cerrahi (konizasyon/LEEP) standarttır."},
            {"key": "B", "text": "Hastayı hiçbir kontrole çağırmadan taburcu etmek", "isCorrect": False, "explanation": "Takipsizlik kansere yol açabilir."},
            {"key": "C", "text": "Yalnızca soğuk su kompresi uygulamak", "isCorrect": False, "explanation": "Neoplaziyi tedavi etmez."},
            {"key": "D", "text": "Sadece yüksek doz vitamin C tableti vermek", "isCorrect": False, "explanation": "Tıbbi cerrahi tedavi şarttır."}
        ])
    ]
    slides.append(make_slide(45, "LSIL ve HSIL Klinik Yönetim Prensipleri", "Konservatif izlem, eksizyonel cerrahi, LEEP, konik biyopsi ve endikasyonlar", "Tedavi ve Klinik Yönetim", s45_narrative, s45_bullets, s45_elements))

    # Slide 46: HSIL Sonrası Uzun Dönem Risk ve İzlem
    s46_narrative = (
        "HSIL nedeniyle cerrahi tedavi (konizasyon veya LEEP) uygulanan hastalar, lezyon tamamen çıkarılmış "
        "olsa dahi ömür boyu jinekolojik takip altında tutulmalıdır.\n\n"
        "- **Alan Kanserleşmesi (Field Cancerization):** Onkojenik HPV genital mukozanın diğer alanlarında da "
        "bulunabilir; bu nedenle HSIL öyküsü olan kadınlarda ilerleyen yıllarda **servikal kanser, vulvar kanser "
        "ve vajinal kanser riski belirgin şekilde artmıştır**.\n"
        "- **Nüks Riski:** Özellikle cerrahi sınırları pozitif olan veya persistan HPV pozitifliği süren kadınlarda "
        "servikal displazi nüks edebilir.\n"
        "- **İzlem Protokolü:** Bu hastalara cerrahi sonrası düzenli sitolojik kontroller ve HPV DNA testleri ile "
        "uzun dönemli periyodik izlem uygulanır.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] HSIL öyküsü olan kadınlarda yalnızca servikal kanser değil; vulvar ve vajinal kanser riski de arttığından düzenli sitolojik ve klinik takip zorunludur."
    )
    s46_bullets = [
        "HSIL öyküsü olan kadınlarda serviks, vulva ve vajina kanseri riski artmıştır.",
        "Persistan viral enfeksiyon alan kanserleşmesine yol açabilir.",
        "Cerrahi sonrası uzun dönem düzenli sitolojik izlem şarttır."
    ]
    s46_elements = [
        make_cloze("HSIL öyküsü bulunan hastalarda genital alanda servikal, vulvar ve vajinal kanser riski artmıştır.", "vajinal kanser", "Alan kanserleşmesiyle riski artan komşu genital kanser"),
        make_table("HSIL Sonrası Kanser Risk Artışı Alanları", ["Genital Bölge", "Histolojik Tür", "Takip Yöntemi"], [
            {"cells": [{"text": "Serviks Korpusu", "isMasked": False}, {"text": "Nüks CIN ve invaziv karsinom", "isMasked": True, "hint": "servikal neoplazi nüksü"}, {"text": "Düzenli Pap smear ve HPV DNA"}]},
            {"cells": [{"text": "Vulva ve Vajina", "isMasked": False}, {"text": "VIN, VAIN ve skuamöz karsinom", "isMasked": False}, {"text": "Detaylı inspeksiyon ve kolposkopik izlem", "isMasked": True, "hint": "dış genital muayene takibi"}]}
        ]),
        make_chain("HSIL Sonrası Uzun Dönem İzlem Aşamaları", [
            "1. Cerrahi Tedavi: Konik biyopsi ile primer HSIL lezyonu eksize edilir.",
            "2. Sınır İncelemesi: Patolog cerrahi sınırların temiz olduğunu doğrular.",
            "3. Periyodik Kontrol: 6. ve 12. aylarda ko-test (Pap smear + HPV) yapılır.",
            "4. Tüm Genital Muayene: Vulva ve vajina mukozası sekonder displaziler yönünden taranır."
        ]),
        make_recall("HSIL öyküsü olan bir kadında uzun dönemde hangi üç anatomik bölgede kanser gelişme riski artmıştır?", "Serviks, vulva ve vajina kanseri riski artmıştır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: HSIL Sonrası İzlem", [
            {"text": "HSIL öyküsü olan kadınlarda servikal kanser riski artmıştır.", "isLie": False, "explanation": "Doğru. Nüks riski devam eder."},
            {"text": "Bu hastalarda vulva ve vajina kanseri gelişme riski de artmıştır.", "isLie": False, "explanation": "Doğru. HPV ilişkili alan kanserleşmesidir."},
            {"text": "Konizasyon olan hastanın bir daha asla ömrü boyunca hiçbir hekime görünmesi gerekmez.", "isLie": True, "explanation": "Tuzak! Risk devam ettiği için düzenli sitolojik ve klinik takip zorunludur."},
            {"text": "Takipte Pap smear ve HPV ko-testi kullanılır.", "isLie": False, "explanation": "Doğru. Rutin izlem protokolüdür."}
        ]),
        make_quiz("HSIL öyküsü bulunan hastalarda uzun dönem takipte riski artan neoplastik tablolar hangileridir?", [
            {"key": "A", "text": "Servikal kanser, vulvar kanser ve vajinal kanser", "isCorrect": True, "explanation": "HSIL öyküsü serviks, vulva ve vajina kanseri riskini artırır."},
            {"key": "B", "text": "Sadece çocukluk çağı retinoblastomu", "isCorrect": False, "explanation": "Retinoblastom çocukluk çağı göz tümörüdür."},
            {"key": "C", "text": "Yalnızca ayak parmaklarında osteom", "isCorrect": False, "explanation": "Kemik tümörleriyle ilgisi yoktur."},
            {"key": "D", "text": "Menenjit ve serebral abse", "isCorrect": False, "explanation": "Santral enfeksiyon tablosudur."}
        ])
    ]
    slides.append(make_slide(46, "HSIL Sonrası Uzun Dönem Risk ve İzlem", "Alan kanserleşmesi, nüks dinamikleri, vulva/vajen riski ve sitolojik takip", "Uzun Dönem Takip ve Onkolojik Risk", s46_narrative, s46_bullets, s46_elements))

    # Slide 47: Pap Testi (Smear): Eksfoliyatif Sitoloji İlkeleri
    s47_narrative = (
        "Papanicolaou (Pap) smear testi, George Papanicolaou tarafından geliştirilen ve onkoloji tarihindeki "
        "en başarılı popülasyon tarama programı kabul edilen **eksfoliyatif sitoloji** yöntemidir.\n\n"
        "- **Biyolojik Prensip:** Displastik ve neoplastik hücrelerin yüzey tutunma molekülleri (kaderinler vb.) zayıflar; "
        "bu hücreler çevre dokulardan kolayca koparak servikal mukusa dökülür (eksfoliasyon).\n"
        "- **Örnekleme Alanı:** Spatül ve endoservikal fırça yardımıyla mutlaka **transformasyon bölgesinden ve "
        "skuamo-kolumnar bileşkeden** 360 derece sürüntü alınmalıdır.\n"
        "- **Preinvaziv Yakalama:** Testin temel amacı kanseri değil, kanserin 10-15 yıl önceki asemptomatik "
        "preinvaziv öncüllerini (SIL/CIN) henüz invazyon olmadan yakalamaktır.\n\n"
        "> [!NOTE]\n"
        "> Pap testi transformasyon bölgesinden dökülen hücrelerin mikroskobik incelemesine dayanan eksfoliyatif sitoloji testidir."
    )
    s47_bullets = [
        "En başarılı kanser tarama testlerinden biridir.",
        "Eksfoliyatif sitoloji prensibiyle çalışır.",
        "Transformasyon bölgesinden hücrelerin kazınması esastır."
    ]
    s47_elements = [
        make_cloze("Pap smear testinde incelenen hücrelerin transformasyon bölgesinden kazınarak dökülmesine eksfoliyatif sitoloji denir.", "eksfoliyatif", "Dökülen hücrelerin incelenmesi prensibi"),
        make_table("Pap Smear Taramasının Temel İlkeleri", ["Özellik", "Uygulama Şekli", "Klinik Hedef"], [
            {"cells": [{"text": "Örnekleme Sahası", "isMasked": False}, {"text": "Transformasyon bölgesi ve SKB", "isMasked": True, "hint": "metaplastik hücresel sınır"}, {"text": "Karsinogenezin başladığı odak"}]},
            {"cells": [{"text": "Teknik", "isMasked": False}, {"text": "Spatül ve fırça ile hücresel kazıma", "isMasked": False}, {"text": "Asemptomatik displastik hücreleri yakalamak", "isMasked": True, "hint": "erken preinvaziv tespit"}]}
        ]),
        make_chain("Pap Smear Test Süreci", [
            "1. Muayene: Spekulum yerleştirilerek serviks doğrudan gözlenir.",
            "2. Kazıma: Fırça ve spatül ile transformasyon zonu yüzeyinden hücreler toplanır.",
            "3. Preparat Hazırlama: Hücreler lam üzerine yayılır veya sıvı bazlı ortama aktarılır.",
            "4. Mikroskobik Tarama: Patolog nükleer genişleme ve hiperkromazi gösteren SIL hücrelerini arar."
        ]),
        make_recall("Pap smear tarama testinin dayandığı temel biyolojik prensip nedir ve hangi anatomik bölgeden örneklenir?", "Eksfoliyatif sitoloji prensibine dayanır; dökülen hücreler transformasyon bölgesinden örneklenir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Pap Testi İlkeleri", [
            {"text": "Pap smear eksfoliyatif sitoloji prensibiyle çalışır.", "isLie": False, "explanation": "Doğru. Dökülen hücreler incelenir."},
            {"text": "Örnekleme transformasyon bölgesinden yapılmalıdır.", "isLie": False, "explanation": "Doğru. Neoplazilerin odak merkezidir."},
            {"text": "Pap smear için hastanın böbreği cerrahi olarak tamamen çıkarılmalıdır.", "isLie": True, "explanation": "Tuzak! Pap smear basit, noninvaziv bir servikal sürüntüdür; böbrekle hiçbir ilgisi yoktur."},
            {"text": "Kanser gelişmeden önceki prekanseröz displaziyi yakalar.", "isLie": False, "explanation": "Doğru. Temel halk sağlığı hedefidir."}
        ]),
        make_quiz("Pap smear testinde yeterli ve kaliteli bir örnekleme yapabilmek için fırça/spatül mutlaka hangi anatomik alana temas etmelidir?", [
            {"key": "A", "text": "Transformasyon bölgesi ve skuamo-kolumnar bileşke", "isCorrect": True, "explanation": "Örnekleme mutlaka transformasyon bölgesini içermelidir."},
            {"key": "B", "text": "Yalnızca over korteksi", "isCorrect": False, "explanation": "Overe ulaşılamaz."},
            {"key": "C", "text": "Rektum mukozası", "isCorrect": False, "explanation": "Gastrointestinal alandır."},
            {"key": "D", "text": "Mesane kubbesi", "isCorrect": False, "explanation": "Üriner sisteme aittir."}
        ])
    ]
    slides.append(make_slide(47, "Pap Testi (Smear): Eksfoliyatif Sitoloji İlkeleri", "Papanicolaou sitolojisi, hücre dökülmesi, transformasyon zonu kazıması ve tarama", "Tarama Yöntemleri: Pap Smear", s47_narrative, s47_bullets, s47_elements))

    # Slide 48: Pap Taramasının Halk Sağlığı Etkisi ve Mortalite Düşüşü
    s48_narrative = (
        "Düzenli Pap smear tarama programlarının yaygınlaştırılması, koruyucu hekimlik ve halk sağlığı "
        "tarihindeki en çarpıcı başarı öykülerinden biridir.\n\n"
        "- **Tarihsel Tablo:** 20. yüzyılın ortalarından önce serviks kanseri, gelişmiş ülkelerde dahi kadınlarda "
        "en sık görülen kanser ilişkili ölüm nedenleri arasında ilk sıralarda yer almaktaydı.\n"
        "- **Mortalite Düşüşü:** Yaygın tarama programlarının uygulanmaya başlanmasıyla birlikte serviks kanseri "
        "ölüm oranlarında **yaklaşık %75'lik devasa bir azalma** kaydedilmiştir.\n"
        "- **Güncel Durum:** Taramanın düzenli yapıldığı toplumlarda serviks kanseri artık önde gelen ölüm nedenleri "
        "arasından çıkmış; preinvaziv evrede kür sağlanan bir hastalık haline gelmiştir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Düzenli Pap smear tarama programları serviks kanseri mortalitesinde yaklaşık %75 azalma sağlamış ve hastalığı önde gelen ölüm nedenleri arasından çıkarmıştır."
    )
    s48_bullets = [
        "Pap taraması serviks kanseri mortalitesinde ~%75 azalma sağlamıştır.",
        "Geçmişte ilk sıralardaki ölüm nedeni günümüzde gerilemiştir.",
        "Hastalık invaziv aşamaya geçmeden preinvaziv evrede yakalanır."
    ]
    s48_elements = [
        make_cloze("Düzenli Pap smear taramaları sayesinde serviks kanseri mortalitesinde yaklaşık yüzde 75 azalma sağlanmıştır.", "yüzde 75", "Mortalitedeki tarihsel azalma yüzdesi"),
        make_table("Pap Smear Taramasının Halk Sağlığı Bilançosu", ["Dönem / Durum", "Kanser Ölüm Sıralaması", "Mortalite Düzeyi"], [
            {"cells": [{"text": "Tarama Öncesi Dönem", "isMasked": False}, {"text": "Kadınlarda önde gelen ölüm nedeni", "isMasked": True, "hint": "en ölümcül jinekolojik kanser"}, {"text": "Yüksek insidans ve fatal seyir"}]},
            {"cells": [{"text": "Tarama Sonrası Dönem", "isMasked": False}, {"text": "Önde gelen ölüm nedenleri arasından çıkmıştır", "isMasked": False}, {"text": "%75 oranında mortalite azalması", "isMasked": True, "hint": "dramatik ölüm oranı düşüşü"}]}
        ]),
        make_chain("Taramadan Toplum Sağlığına", [
            "1. Popülasyon Taraması: Kadınlar semptomsuzken 3-5 yılda bir Pap smear verir.",
            "2. Preinvaziv Müdahale: CIN II/III aşamasındaki lezyonlar konizasyonla temizlenir.",
            "3. İnvazyonun Önlenmesi: Yıllar içinde gelişecek invaziv skuamöz karsinomlar engellenir.",
            "4. %75 Başarı: Toplum düzeyinde serviks kanseri mortalitesi %75 geriler."
        ]),
        make_recall("Düzenli Pap smear tarama programlarının kadın sağlığı ve serviks kanseri mortalitesi üzerindeki halk sağlığı etkisi nedir?", "Ölüm oranlarında yaklaşık %75 azalma sağlamış ve serviks kanserini önde gelen ölüm nedenleri arasından çıkarmıştır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Pap Taraması Halk Sağlığı Etkisi", [
            {"text": "Pap smear serviks kanseri ölüm oranlarında yaklaşık %75 azalma sağlamıştır.", "isLie": False, "explanation": "Doğru. Tarihsel mortalite düşüşüdür."},
            {"text": "Geçmişte önde gelen ölüm nedeniyken günümüzde gerilemiştir.", "isLie": False, "explanation": "Doğru. Tarama sayesinde sırası düşmüştür."},
            {"text": "Pap smear taraması başladıktan sonra kadınlarda kanser ölümleri %800 katlanarak artmıştır.", "isLie": True, "explanation": "Tuzak! Tam aksine ölümler %75 oranında azalmıştır."},
            {"text": "Başarı preinvaziv lezyonların invazyon öncesi yakalanmasından kaynaklanır.", "isLie": False, "explanation": "Doğru. Erken yakalama esastır."}
        ]),
        make_quiz("Düzenli Pap smear tarama programlarının yaygınlaştırılması serviks kanseri mortalitesinde yaklaşık ne kadarlık bir azalma sağlamıştır?", [
            {"key": "A", "text": "Yaklaşık %75 azalma", "isCorrect": True, "explanation": "Pap smear mortalitede yaklaşık %75 düşüş sağlamıştır."},
            {"key": "B", "text": "%0 (Hiçbir faydası olmamıştır)", "isCorrect": False, "explanation": "Tarihteki en başarılı taramadır."},
            {"key": "C", "text": "%1'den az", "isCorrect": False, "explanation": "Düşüş çok belirgindir (%75)."},
            {"key": "D", "text": "Ölümleri iki katına çıkarmıştır", "isCorrect": False, "explanation": "Ölümleri dramatik biçimde azaltmıştır."}
        ])
    ]
    slides.append(make_slide(48, "Pap Taramasının Halk Sağlığı Etkisi ve Mortalite Düşüşü", "Tarihsel başarı, %75 mortalite düşüşü, koruyucu onkoloji ve halk sağlığı", "Halk Sağlığı ve Epidemiyoloji", s48_narrative, s48_bullets, s48_elements))

    # Slide 49: Kaynak Kısıtlı Ülkelerde Serviks Kanseri Yükü
    s49_narrative = (
        "Pap smear taramasının başarısı gelişmiş ülkelerde kanıtlanmış olsa da, dünya genelindeki "
        "kanser yükü dağılımı ciddi bir küresel eşitsizlik sergilemektedir.\n\n"
        "- **Küresel Eşitsizlik:** Dünya genelinde her yıl teşhis edilen yeni serviks kanseri olgularının "
        "**>%85'i kaynak kısıtlı ve az gelişmiş ülkelerde** görülmektedir.\n"
        "- **Nedenler:** Sağlık altyapısı eksikliği, organize tarama programlarının bulunmaması, sitopatolog ve "
        "laboratuvar yetersizliği kadınların tanı alamamasına yol açar.\n"
        "- **Klinik Tablo:** Bu ülkelerde kadınlar preinvaziv evrede değil; masif kanama, ileri evre pelvik "
        "kitle ve üremi gibi terminal komplikasyonlarla hastaneye başvurmaktadır.\n\n"
        "> [!NOTE]\n"
        "> Dünyadaki yeni serviks kanseri olgularının %85'ten fazlası organize tarama programlarının olmadığı kaynak kısıtlı ülkelerdedir."
    )
    s49_bullets = [
        "Yeni serviks kanseri olgularının >%85'i kaynak kısıtlı ülkelerdedir.",
        "Organize tarama programlarının eksikliği temel nedendir.",
        "Hastalar preinvaziv evrede değil, terminal aşamada başvurur."
    ]
    s49_elements = [
        make_cloze("Dünya genelindeki yeni serviks kanseri olgularının yüzde 85'ten fazlası kaynak kısıtlı ülkelerde görülmektedir.", "yüzde 85", "Az gelişmiş ülkelerdeki olgu oranı"),
        make_table("Coğrafi Dağılım ve Tarama Etkisi", ["Ülke Grubu", "Yeni Olgu Oranı", "Klinik Başvuru Evresi"], [
            {"cells": [{"text": "Gelişmiş Ülkeler", "isMasked": False}, {"text": "Tüm olguların <%15'i", "isMasked": False}, {"text": "Asemptomatik preinvaziv evre (SIL)", "isMasked": True, "hint": "erken tarama evresi"}]},
            {"cells": [{"text": "Kaynak Kısıtlı Ülkeler", "isMasked": False}, {"text": "Tüm olguların >%85'i", "isMasked": True, "hint": "ezici küresel çoğunluk"}, {"text": "İleri evre invaziv karsinom", "isMasked": False}]}
        ]),
        make_chain("Tarama Yokluğundan Terminal Kansere", [
            "1. Altyapı Yokluğu: Bölgede rutin Pap smear tarama ağı bulunmamaktadır.",
            "2. Sessiz Progresyon: HPV enfeksiyonu 10 yıl boyunca fark edilmeden HSIL'e ilerler.",
            "3. İnvazyon: Lezyon stromaya girerek geniş bir kitle oluşturur.",
            "4. Geç Başvuru: Hasta ileri evrede masif kanamayla hekime ulaşır."
        ]),
        make_recall("Dünya genelinde teşhis edilen yeni serviks kanseri olgularının yüzde kaçı organize tarama altyapısı bulunmayan kaynak kısıtlı ülkelerdedir?", "Olguların %85'ten fazlası kaynak kısıtlı ülkelerdedir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Küresel Serviks Kanseri Yükü", [
            {"text": "Yeni serviks kanseri olgularının >%85'i kaynak kısıtlı ülkelerdedir.", "isLie": False, "explanation": "Doğru. Küresel yükün ezici çoğunluğudur."},
            {"text": "Organize tarama programlarının olmaması en temel risk faktörüdür.", "isLie": False, "explanation": "Doğru. Tarama yokluğu ilerlemeye zemin hazırlar."},
            {"text": "Az gelişmiş ülkelerde serviks kanseri tamamen yok edilmiş bir hastalıktır.", "isLie": True, "explanation": "Tuzak! Tam aksine dünyadaki olguların %85'inden fazlası bu ülkelerdedir ve ölüm oranı çok yüksektir."},
            {"text": "Taraması eksik toplumlarda hastalar ileri evrede hekime ulaşır.", "isLie": False, "explanation": "Doğru. Semptomatik evrede başvururlar."}
        ]),
        make_quiz("Dünya genelindeki yeni invaziv serviks karsinomu olgularının coğrafi dağılımı ile ilgili aşağıdakilerden hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Yeni olguların %85'ten fazlası kaynak kısıtlı ülkelerdedir", "isCorrect": True, "explanation": "Organize taraması olmayan kaynak kısıtlı ülkeler olguların >%85'ini oluşturur."},
            {"key": "B", "text": "Olguların tamamı yalnızca Antarktika'daki araştırma istasyonlarındadır", "isCorrect": False, "explanation": "Gerçek dışı coğrafi iddiadır."},
            {"key": "C", "text": "Gelişmiş ülkelerde mortalite az gelişmiş ülkelerden 500 kat daha fazladır", "isCorrect": False, "explanation": "Tam tersi geçerlidir."},
            {"key": "D", "text": "Dünyada serviks kanseri diye bir hastalık kalmamıştır", "isCorrect": False, "explanation": "Hastalık küresel olarak devam etmektedir."}
        ])
    ]
    slides.append(make_slide(49, "Kaynak Kısıtlı Ülkelerde Serviks Kanseri Yükü", "Küresel eşitsizlik, >%85 insidans, altyapı yetersizliği ve geç klinik başvuru", "Küresel Onkoloji", s49_narrative, s49_bullets, s49_elements))

    # Slide 50: [TEKRAR SAYFASI - CHECKPOINT 5] SIL Yaş Dağılımı, Kolposkopi ve Pap Taraması
    s50_narrative = (
        "Bölüm 5'te servikal prekanseröz lezyonların zaman çizelgesini, kolposkopik tanısal incelikleri "
        "ve Pap smear taramasının halk sağlığı zaferini kapsamlı biçimde konsolide ettik.\n\n"
        "- **Zirve Yaşları:** SIL insidansı **yaklaşık 30 yaşta** zirve yaparken; invaziv karsinom **10-15 yıl sonra "
        "yaklaşık 45 yaş civarında** zirveye ulaşır; bu aralık tarama için altın fırsattır.\n"
        "- **Kolposkopi ve Asetobeyaz Reaksiyon:** %3-5 asetik asit uygulandığında displastik hücrelerin artmış "
        "nükleer proteinleri çökelir ve lezyon **asetobeyaz** renkte parlayarak punch biyopsiyi hedefler.\n"
        "- **Yönetim Ayrımı:** Biyopsiyle doğrulanmış LSIL'de **konservatif takip** esasken; HSIL veya kalıcı LSIL'de "
        "**cerrahi eksizyon (konik biyopsi / LEEP)** yapılır; takipte vulva/vajen kanseri riski akılda tutulur.\n"
        "- **Pap Smear Zaferi:** Eksfoliyatif sitoloji mortalitede **%75 azalma** sağlamıştır; ancak olguların **>%85'i "
        "hala tarama altyapısı eksik kaynak kısıtlı ülkelerdedir**.\n\n"
        "> [!IMPORTANT]\n"
        "> [BÖLÜM 5 SENTEZİ] SIL 30 yaşta, kanser 45 yaşta zirve yapar; asetik asit nükleer proteinleri çökelterek biyopsi yerini gösterir; Pap smear ölümleri %75 azaltmıştır fakat kaynak kısıtlı ülkeler küresel yükün %85'ini taşır."
    )
    s50_bullets = [
        "SIL ~30 yaşta, kanser ~45 yaşta zirve yapar (10-15 yıllık pencere).",
        "Asetik asit nükleer proteinleri çökelterek asetobeyaz epitel oluşturur.",
        "LSIL konservatif izlenir; HSIL konik biyopsi ile eksize edilir.",
        "Pap smear ölümleri %75 azalttı; ancak olguların >%85'i kaynak kısıtlı ülkelerdedir."
    ]
    s50_elements = [
        make_cloze("Pap smear taramasının yaygınlaşması ile serviks kanseri mortalitesinde yaklaşık yüzde 75 azalma sağlanmıştır.", "yüzde 75", "Bölüm 5 sentezinde pekiştirilen mortalite düşüş yüzdesi"),
        make_table("Bölüm 5 Klinik ve Epidemiyolojik Sentez Tablosu", ["Konu / Parametre", "Temel Değer / Bulgu", "Klinik / Halk Sağlığı Önemi"], [
            {"cells": [{"text": "Mortalite Değişimi", "isMasked": False}, {"text": "%75 mortalite düşüşü", "isMasked": True, "hint": "tarihsel azalma oranı"}, {"text": "Pap smear taramasının küresel başarısı"}]},
            {"cells": [{"text": "Kolposkopik Belirteç", "isMasked": False}, {"text": "Opak asetobeyaz reaksiyon", "isMasked": False}, {"text": "Artmış nükleer protein çökmesiyle hedef biyopsi", "isMasked": True, "hint": "protein çökmesiyle odak saptama"}]},
            {"cells": [{"text": "Küresel Olgu Yükü", "isMasked": False}, {"text": "Kaynak kısıtlı ülkelerde >%85", "isMasked": True, "hint": "küresel dağılım oranı"}, {"text": "Tarama eşitsizliğinin acı bilançosu"}]}
        ]),
        make_chain("Bölüm 5 Süreç Entegrasyonu", [
            "1. Yaş Penceresi: 30 yaşta saptanan SIL, 45 yaştaki invaziv kansere dönüşmeden önce yakalanmalıdır.",
            "2. Görsel Vurgulama: Kolposkopide asetik asit sürülerek asetobeyaz odak işaretlenir.",
            "3. Histolojik Yönetim: Biyopsi HSIL gelirse konik biyopsi ile tam eksizyon sağlanır.",
            "4. Toplum Boyutu: Bu tarama zinciri sayesinde mortalite %75 geriletilmiştir."
        ]),
        make_recall("Bölüm 5 boyunca öğrendiğimiz: (1) SIL ve kanser pik yaşları, (2) Kolposkopide beyazlaşma nedeni ve (3) Pap smear mortalite düşüş oranı nedir?", "(1) SIL ~30 yaş, kanser ~45 yaş, (2) Artmış nükleer proteinlerin çökmesi, (3) %75 mortalite azalmasıdır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Bölüm 5 Checkpoint Sentezi", [
            {"text": "SIL ~30 yaşta, invaziv karsinom ~45 yaş civarında zirve yapar.", "isLie": False, "explanation": "Doğru. İki zirve arasında 10-15 yıl vardır."},
            {"text": "Kolposkopide lezyonlar asetik asit uygulaması ile vurgulanır.", "isLie": False, "explanation": "Doğru. Asetobeyaz reaksiyon verir."},
            {"text": "Pap smear taraması dünyada sadece erkeklerde prostat kanserini sıfırlamıştır.", "isLie": True, "explanation": "Tuzak! Pap smear kadınlarda serviks kanserini tarar; erkek veya prostatla ilgisi yoktur."},
            {"text": "Yeni serviks kanseri olgularının >%85'i kaynak kısıtlı ülkelerdedir.", "isLie": False, "explanation": "Doğru. Küresel dağılım eşitsizliğidir."}
        ]),
        make_quiz("Bölüm 5'te pekiştirilen klinik ve halk sağlığı prensiplerine göre aşağıdakilerden hangisi YANLIŞTIR?", [
            {"key": "A", "text": "Pap smear taraması serviks kanseri ölüm oranlarında hiçbir değişiklik yapmamıştır", "isCorrect": True, "explanation": "Yanlış önerme! Ölüm oranlarında %75 gibi devasa bir azalma sağlamıştır."},
            {"key": "B", "text": "SIL genellikle asemptomatiktir ve rutin taramada yakalanır", "isCorrect": False, "explanation": "Doğru bilgidir."},
            {"key": "C", "text": "Kolposkopide asetik asit nükleer proteinleri çökelterek beyaz görünüm verir", "isCorrect": False, "explanation": "Doğru bilgidir."},
            {"key": "D", "text": "Biyopsiyle doğrulanmış HSIL cerrahi eksizyon ile tedavi edilir", "isCorrect": False, "explanation": "Doğru bilgidir."}
        ])
    ]
    slides.append(make_slide(50, "[TEKRAR SAYFASI - CHECKPOINT 5] SIL Yaş Dağılımı, Kolposkopi ve Pap Taraması", "Bölüm 5 kapsamlı tekrarı: yaş pikleri, asetobeyaz reaksiyon, yönetim ve küresel yük", "Bölüm Tekrarı ve Konsolidasyon", s50_narrative, s50_bullets, s50_elements))

    return slides

if __name__ == '__main__':
    slides = get_sec5()
    print(f"Sec5 generated: {len(slides)} slides (Slide 41 to 50)")
    for s in slides:
        print(f" - Slide {s['slideNumber']}: {s['title']} ({len(s['interactiveElements'])} elements, {len(s['content'].split())} words)")
