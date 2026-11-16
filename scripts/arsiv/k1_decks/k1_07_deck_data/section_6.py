"""
Bölüm 6: Glikojen Depolanması ve Glikojen Depo Hastalıkları (Glikojenozlar)
Adımlar: 51 - 60
Checkpoint: Adım 59 (3 Akıl Kartı)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_6_slides():
    slides = []

    # ADIM 51
    slides.append({
        "slideNumber": 51,
        "title": "Glikojen Metabolizması ve Hücresel Rezerv Dinamiği",
        "subtitle": "Glukozun polimerizasyonu, dallanmış enerji deposu ve lizozomal döngü",
        "badge": "Glikojen Biyolojisi",
        "badgeColor": "amber",
        "synthesisNarrative": (
            "Glikojen, memeli hücrelerinde glukozun acil kullanım için polimerize edildiği dallanmış bir polisakkarit "
            "formudur. Başlıca karaciğerde (tüm vücudun kan şekerini dengelemek üzere) ve iskelet kasında (kas "
            "kasılması sırasında lokal enerji sağlamak üzere) depolanır. Normalde sitozolde küçük granüller halinde bulunur "
            "ve insülin-glukagon ekseninde sentez (glikogenez) ve yıkım (glikojenoliz) döngüsü sürdürülür.\n\n"
            "> [TEMEL İLKE] Hücre içi glikojen metabolizmasının küçük bir kısmı (otofaji yoluyla) lizozomlarda asit "
            "alfa-glukozidaz (asit maltaz) tarafından parçalanır.\n\n"
            "Glukoz metabolizmasındaki sistemik dengesizlikler (diyabet) veya özgül enzim eksiklikleri (glikojenozlar) "
            "glikojenin aşırı depolanmasına yol açar."
        ),
        "medicalTerms": [
            {"term": "Glikojen", "explanation": "Glukoz birimlerinin alfa-1,4 ve alfa-1,6 bağlarıyla birbirine bağlandığı dallı depo polisakkaritidir."},
            {"term": "Glikojenoliz", "explanation": "Glikojen polimerinin glukoz veya glukoz-1-fosfata parçalanması sürecidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Glikojen primer olarak karaciğer ve iskelet kasında depolanır.",
            "📌 [SINAV SPOTU] Glikojenin lizozomal yıkımından asit alfa-glukozidaz (asit maltaz) sorumludur."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Dallı Polimer", "desc": "Hızlı glukoz salınımı için çok uçlu moleküler mimari.", "isKey": True},
                {"title": "Çifte Yıkım", "desc": "Sitozolik fosforilazlar ve lizozomal asit maltaz yolağı.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Memeli hücrelerinde glukoz moleküllerinin polimerize edilerek depolandığı dallı polisakkarit yapısına glikojen adı verilir.",
                "glikojen",
                "Hücresel enerji rezervi olan dallı glukoz polimeri"
            ),
            make_active_recall(
                "İnsan vücudunda glikojenin en yoğun olarak depolandığı iki temel organ hangisidir?",
                "Karaciğer parankimi ve iskelet kası lifleridir."
            )
        ]
    })

    # ADIM 52
    slides.append({
        "slideNumber": 52,
        "title": "Glikojenin Işık Mikroskopisindeki Morfolojisi ve PAS / Diyastaz Reaksiyonu",
        "subtitle": "Rutin fiksasyonda berrak vakuol görünümü ve histokimyasal sindirim testi",
        "badge": "Histokimya ve PAS",
        "badgeColor": "purple",
        "synthesisNarrative": (
            "Glikojen suda yüksek oranda çözünür bir polisakkarittir. Standart sulu formalin fiksasyonunda glikojen "
            "kolayca eriyip gittiğinden, rutin hematoksilen-eozin (H&E) kesitlerinde sitoplazma optik olarak boş, "
            "soluk, vakuollü veya 'berrak hücre' (clear cell) şeklinde görünür. Bu nedenle lipidden veya sudan ayırt "
            "edilebilmesi için özel histokimyasal yöntemler kullanılır.\n\n"
            "> [SINAV SPOTU] Glikojen Periyodik Asit-Schiff (PAS) boyası ile koyu mor-eflatun (magenta) boyanır; "
            "dokunun amilaz (diyastaz) enzimiyle önceden sindirilmesi durumunda bu boyanma tamamen kaybolur (PAS+, diyastaz duyarlı).\n\n"
            "Bu özellik glikojeni, diyastaza dirençli olan müsin ve α1-antitripsin gibi diğer PAS(+) maddelerden kesin olarak ayırır."
        ),
        "medicalTerms": [
            {"term": "Periyodik Asit-Schiff (PAS)", "explanation": "Glikojen, glikoprotein ve polisakkaritleri magenta rengine boyayan histokimyasal reaksiyondur."},
            {"term": "Diyastaz Duyarlılığı", "explanation": "Amilaz enzimiyle dokudaki glikojenin eritilmesi ve PAS boyanmasının silinmesidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Glikojen PAS ile pozitif boyanır ve diyastaz sindirimi ile bu boyanma kaybolur.",
            "📌 [SINAV SPOTU] Diyastaza dirençli PAS(+) granüller α1-antitripsini, duyarlı olanlar ise glikojeni gösterir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "H&E Görünümü", "desc": "Optik olarak boş, soluk veya berrak vakuollü sitoplazma.", "isKey": True},
                {"title": "PAS-Diyastaz Testi", "desc": "PAS pozitif + diyastaz duyarlı = Glikojen.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Madde", "H&E Görünümü", "PAS Boyası", "PAS + Diyastaz Uygulaması"],
                [
                    [("Glikojen", False, ""), ("Berrak / Vakuollü", False, ""), ("Kuvvetli Pozitif (Mor)", False, ""), ("Negatif (Boya silinir, duyarlıdır)", True, "Amilaz enzimiyle eriyen polisakkarit")],
                    [("α1-Antitripsin", False, ""), ("Eozinofilik homojen küre", False, ""), ("Kuvvetli Pozitif (Mor)", False, ""), ("Pozitif kalır (Dirençlidir)", True, "Sindirimden etkilenmeyen mutant glikoprotein")],
                    [("Nötral Lipid (Steatoz)", False, ""), ("Boş yuvarlak vakuol", False, ""), ("Negatif (Boyanmaz)", False, ""), ("Negatif (Önemsiz)", False, "")]
                ]
            ),
            make_cloze(
                "Glikojen birikimi olan bir doku kesitinde PAS boyanması doku amilaz enzimi ile sindirildiğinde kaybolur.",
                "amilaz",
                "Glikojeni parçalayarak PAS boyasını silen diyastaz enzimi"
            )
        ]
    })

    # ADIM 53
    slides.append({
        "slideNumber": 53,
        "title": "Diabetes Mellitus'ta Glikojen: Proksimal Tübüller (Armanni-Ebstein Hücreleri)",
        "subtitle": "Aşırı glukozüri, tübüler glukoz yüklenmesi ve vakuolizasyon",
        "badge": "Armanni-Ebstein",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Diabetes mellitus hastalarında kontrolsüz hiperglisemi (kan glukozunun renal eşik olan 180 mg/dL'yi aşması) "
            "durumunda idrar filtratına aşırı glukoz dökülür (glukozüri). Henle kulpunun inen kolu ve böbrek proksimal "
            "tübül epitel hücreleri lümendeki aşırı glukozu SGLT2 taşıyıcılarıyla yoğun şekilde geri emer.\n\n"
            "> [SINAV SPOTU] Tübül hücreleri sitoplazmalarında aşırı glukozu glikojene dönüştürerek depolar; sitoplazma "
            "şişer, berraklaşır ve bu hücrelere 'Armanni-Ebstein hücreleri' adı verilir.\n\n"
            "Armanni-Ebstein lezyonu diyabetik ketoasidoz ve ağır dekompanse diyabetin klasik histopatolojik göstergesidir "
            "ve glisemik kontrol sağlandığında tamamen geriler."
        ),
        "medicalTerms": [
            {"term": "Armanni-Ebstein Hücresi", "explanation": "Ağır diyabette glukozüriye yanıt olarak glikojen depolayıp berraklaşan böbrek tübül hücresidir."},
            {"term": "Glukozüri", "explanation": "Kan şekeri böbrek eşiğini aştığında idrara glukoz çıkması durumudur."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Armanni-Ebstein lezyonu böbrek tübüllerinde glikojen birikimidir.",
            "📌 [SINAV SPOTU] Kötü kontrollü diabetes mellitus ve ketoasidozda görülür."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Lokalizasyon", "desc": "Proksimal tübül epiteli ve Henle kulpunun inen kolu.", "isKey": True},
                {"title": "Histopatoloji", "desc": "Sitoplazmada PAS(+) glikojenle şişmiş berrak epitel hücreleri.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_micro_quiz(
                "Ağır diyabetik ketoasidoz koması nedeniyle vefat eden bir hastanın otopsisinde böbrek proksimal tübül epitel hücrelerinin berrak ve vakuollü olduğu, PAS boyasında koyu mor boyanıp diyastaz ile boyanmanın kaybolduğu saptanıyor (Armanni-Ebstein lezyonu). Bu hücrelerde biriken madde hangisidir?",
                {
                    "A": "Nötral trigliseridler",
                    "B": "Glikojen",
                    "C": "Kolesteril esterler",
                    "D": "Amiloid proteinleri",
                    "E": "Hemosiderin pigmenti"
                },
                "B",
                {
                    "A": "Trigliseridler PAS ile boyanmaz ve Armanni-Ebstein hücresini oluşturmaz.",
                    "B": "Doğru! Armanni-Ebstein lezyonu ağır diyabette proksimal tübülde biriken glikojendir.",
                    "C": "Kolesterol safra kesesi veya ateromda köpük hücre yapar.",
                    "D": "Amiloid Kongo kırmızısı tutar, diyastazla erimez.",
                    "E": "Hemosiderin Prusya mavisiyle boyanan demir pigmentidir."
                }
            ),
            make_cloze(
                "Kötü kontrollü diyabette böbrek tübül hücrelerinde glikojen birikmesiyle oluşan morfolojik yapıya Armanni-Ebstein lezyonu denir.",
                "Armanni-Ebstein",
                "Diyabetik böbrek tübülündeki glikojenli hücre lezyonunun adı"
            )
        ]
    })

    # ADIM 54
    slides.append({
        "slideNumber": 54,
        "title": "Diyabette Hepatosit ve Pankreas Beta Hücrelerinde Glikojen",
        "subtitle": "Glikojenli nükleuslar, kardiyomiyosit infiltrasyonu ve Langerhans dejenerasyonu",
        "badge": "Organ Tutulumları",
        "badgeColor": "blue",
        "synthesisNarrative": (
            "Diyabette glikojen depolanması böbrek tübülleriyle sınırlı kalmaz. Karaciğer parankiminde hepatositler aşırı "
            "glukoz yükü altında hem sitoplazmalarında hem de çekirdeklerinde glikojen biriktirir. Işık mikroskobunda "
            "hepatosit çekirdeklerinin vakuollü, şiş ve berrak görünmesine 'glikojenli nükleus' adı verilir.\n\n"
            "> [YÜKSEK VERİM] Pankreasın Langerhans adacıklarındaki beta hücrelerinde glikojen depolanması 'hidropik "
            "dejenerasyon' oluşturur ve insülin salgılama rezervini daha da baltalar.\n\n"
            "Ayrıca kalp kası liflerinde de glikojen depolanabilir; bu durum diyabetik kardiyomiyopatinin hücresel "
            "bileşenlerinden birini teşkil eder."
        ),
        "medicalTerms": [
            {"term": "Glikojenli Nükleus", "explanation": "Diyabet gibi durumlarda çekirdek içine glikojen infiltrasyonuyla nükleusun berraklaşmasıdır."},
            {"term": "Hidropik Dejenerasyon", "explanation": "Pankreas beta hücrelerinde glikojen yüklenmesiyle hücrenin şişip berraklaşmasıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Karaciğerde glikojenli nükleuslar diabetes mellitusun karakteristik histolojik bulgusudur.",
            "📌 [SINAV SPOTU] Pankreas beta hücrelerinde glikojen yüklenmesi hidropik vakuolizasyon yapar."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Hepatosit Çekirdeği", "desc": "Nükleus içine glikojen sızması ve berraklaşma.", "isKey": True},
                {"title": "Pankreas Adacığı", "desc": "Beta hücrelerinde glikojenik şişme ve insülinopoez azalması.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "Normal Hepatosit Çekirdeği vs Glikojenli Nükleus",
                "Normal Hepatosit Çekirdeği",
                "Düzgün nükleer membran, homojen kromatin dağılımı ve belirgin nükleolus içeren mor-mavi çekirdek.",
                "Glikojenli Nükleus (Diyabet)",
                "İçine glikojen infiltre olmuş, kromatini kenara itilmiş, ortası optik olarak boş ve berrak şişkin çekirdek."
            ),
            make_active_recall(
                "Diabetes mellituslu bir hastanın karaciğer biyopsisinde çekirdekte izlenen tipik morfolojik değişiklik nedir?",
                "Glikojenli nükleustur (çekirdek içine glikojen birikimiyle nükleusun vakuollü ve berrak görünmesi)."
            )
        ]
    })

    # ADIM 55
    slides.append({
        "slideNumber": 55,
        "title": "Glikojen Depo Hastalıkları (Glikojenozlar): Enzim Defektleri ve Kalıtım",
        "subtitle": "Kalıtsal enzim eksiklikleri ve karaciğer, kas veya sistemik depolanma kalıpları",
        "badge": "Glikojenozlar",
        "badgeColor": "teal",
        "synthesisNarrative": (
            "Glikojen depo hastalıkları (glikojenozlar), glikojen sentezi, dallanması veya parçalanmasında görev alan "
            "enzimlerin kalıtsal yokluğundan kaynaklanan otozomal resesif geçişli metabolik bozukluklar grubudur. "
            "Klinik tablo eksik olan enzimin doku dağılımına göre iki ana gruba ayrılır: hepatik formlar (hipoglisemi "
            "ve hepatomegali) ve miyopatik formlar (egzersiz intoleransı, kas krampları).\n\n"
            "> [TEMEL İLKE] Hepatik formların prototipi Tip I (Von Gierke), miyopatik formların prototipi Tip V (McArdle), "
            "lizozomal yaygın formun prototipi ise Tip II (Pompe) hastalığıdır.\n\n"
            "Bu hastalıklarda biriken glikojen normal yapıda olabileceği gibi dallanma/budanma enzim defektlerinde anormal "
            "polimer yapısında da olabilir."
        ),
        "medicalTerms": [
            {"term": "Glikojen Depo Hastalığı", "explanation": "Glikojen metabolizma enzimlerinin kalıtsal yokluğunda dokularda glikojen birikmesiyle giden tablolardır."},
            {"term": "Otozomal Resesif", "explanation": "Glikojenozların büyük çoğunluğunun kalıtım modelidir (her iki ebeveynden mutant alel geçişi)."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Glikojenozlar hepatik form, miyopatik form ve lizozomal form olarak ayrılır.",
            "📌 [SINAV SPOTU] Karaciğer enzim defektleri açlık hipoglisemisi, kas enzim defektleri kramp ve miyoglobinüri yapar."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Hepatik Form", "desc": "Glukoz salınamaz, kan şekeri düşer, karaciğer devasa büyür.", "isKey": True},
                {"title": "Miyopatik Form", "desc": "Kas enerji üretemez, kramp ve egzersiz intoleransı gelişir.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Glikojen depo hastalıklarının hepatik formlarında karaciğerden kana serbest glukoz verilemediği için açlık hipoglisemisi gelişir.",
                "hipoglisemisi",
                "Karaciğer kaynaklı glukoz eksikliğinde kanda şekerin düşmesi"
            ),
            make_active_recall(
                "Glikojenozların karaciğer tutulumu gösteren hepatik formları ile kas tutulumu gösteren miyopatik formlarının temel klinik farkı nedir?",
                "Hepatik formlar açlık hipoglisemisi ve hepatomegali ile seyrederken; miyopatik formlar kas güçsüzlüğü, egzersiz krampları ve rabdomiyoliz ile seyreder."
            )
        ]
    })

    # ADIM 56
    slides.append({
        "slideNumber": 56,
        "title": "Tip I Glikojenoz (Von Gierke): Glukoz-6-Fosfataz ve Masif Hepatomegali",
        "subtitle": "Açlık hipoglisemisi, laktik asidoz, hiperürisemi ve renomegali mekanizması",
        "badge": "Von Gierke (Tip I)",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Von Gierke hastalığı (Tip I glikojen depo hastalığı), glukoz-6-fosfatı serbest glukoza dönüştüren glukoz-6-fosfataz "
            "(G6Paz) enziminin genetik eksikliğidir. G6Paz hem glikojenolizin hem de glukoneogenezin son ortak enzimi "
            "olduğu için karaciğer kana kesinlikle serbest glukoz veremez.\n\n"
            "> [SINAV SPOTU] Karaciğer ve böbrek proksimal tübülleri glikojenle dolar; masif hepatomegali ve renomegali "
            "gelişir. Ancak kas dokusunda G6Paz fizyolojik olarak zaten bulunmadığı için iskelet kası normaldir.\n\n"
            "Hastada ağır açlık hipoglisemisi, laktik asidoz, hiperürisemi (gut krizleri) ve hiperlipidemi tablosu görülür."
        ),
        "medicalTerms": [
            {"term": "Von Gierke Hastalığı (Tip I)", "explanation": "Glukoz-6-fosfataz eksikliğine bağlı masif hepatomegali ve hipoglisemiyle seyreden hastalıktır."},
            {"term": "Glukoz-6-Fosfataz", "explanation": "Glikojenoliz ve glukoneogenezin son basamağında kana serbest glukoz çıkaran anahtar enzimdir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Von Gierke'de eksik enzim glukoz-6-fosfatazdır.",
            "📌 [SINAV SPOTU] Karaciğer ve böbrekler glikojenle büyür; kasta birikim olmaz."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Enzim Eksikliği", "desc": "Glukoz-6-fosfataz (karaciğer ve böbrekte bulunur).", "isKey": True},
                {"title": "Klinik Tetrad", "desc": "Şiddetli açlık hipoglisemisi, laktik asidoz, hiperürisemi, hiperlipidemi.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_causal_chain(
                "Von Gierke Hastalığında Metabolik Kriz Zinciri",
                [
                    "1. G6Paz Eksikliği: Hepatosit glukoz-6-fosfatı serbest glukoza çeviremez.",
                    "2. Glikojen Göllenmesi: Glukoz-6-fosfat glikojen sentezini kamçılar; karaciğer devasa büyür.",
                    "3. Açlık Hipoglisemisi: Kana glukoz verilemediği için açlıkta nöbet geçirtecek hipoglisemi gelişir.",
                    "4. Şant Yolları: Biriken G6P glikolize kayarak laktik asidoza, heksoz monofosfata kayarak hiperürisemiye yol açar."
                ]
            ),
            make_cloze(
                "Von Gierke hastalığında glikojen depolanması başlıca karaciğer ve böbrekler organlarında görülür.",
                "böbrekler",
                "Karaciğer dışında G6Paz içeren ve glikojenle büyüyen retroperitoneal organ"
            )
        ]
    })

    # ADIM 57
    slides.append({
        "slideNumber": 57,
        "title": "Tip II Glikojenoz (Pompe): Lizozomal Asit Maltaz (GAA) ve Kardiyomegali",
        "subtitle": "Lizozomal depo hastalığı niteliğindeki tek glikojenoz ve erken bebeklik kalp yetmezliği",
        "badge": "Pompe (Tip II)",
        "badgeColor": "purple",
        "synthesisNarrative": (
            "Pompe hastalığı (Tip II glikojen depo hastalığı), glikojenozlar ailesinin en benzersiz üyesidir; çünkü "
            "eksik olan enzim sitozolik değil, lizozomal bir hidrolaz olan asit alfa-glukozidazdır (asit maltaz / GAA). "
            "Bu nedenle Pompe hastalığı hem bir glikojenoz hem de tam anlamıyla bir lizozomal depo hastalığıdır.\n\n"
            "> [SINAV SPOTU] Tüm doku lizozomlarında glikojen birikir; ancak en ölümcül darbeyi kalp kası alır. "
            "Masif kardiyomegali, kardiyomiyopati ve hipotoni gelişir; tedavi edilmeyen bebekler 1-2 yaşta kalp yetersizliğinden kaybedilir.\n\n"
            "Kan şekeri düzeyleri tamamen normaldir; çünkü sitozolik glikojenoliz enzimleri eksiksiz çalışmaktadır."
        ),
        "medicalTerms": [
            {"term": "Pompe Hastalığı (Tip II)", "explanation": "Lizozomal asit alfa-glukozidaz eksikliğinde masif kardiyomegali ve hipotoniyle seyreden hastalıktır."},
            {"term": "Asit Alfa-Glukozidaz (GAA)", "explanation": "Lizozom lümeninde otofajiyle gelen glikojeni glukoza parçalayan hidrolazdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Pompe hastalığı lizozomal enzim eksikliğiyle giden tek glikojenozdur.",
            "📌 [SINAV SPOTU] Kan şekeri normaldir; en tipik bulgu masif kardiyomegali ve erken kalp yetmezliğidir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Enzim Defekti", "desc": "Lizozomal asit alfa-glukozidaz (asit maltaz).", "isKey": True},
                {"title": "Hedef Organ", "desc": "Miyokard (kalp) ve iskelet kası lizozomları.", "isKey": True},
                {"title": "Normoglisemi", "desc": "Sitozolik glikojenoliz sağlam olduğu için kan şekeri normaldir.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_micro_quiz(
                "4 aylık bir bebekte ağır kas güçsüzlüğü (hipotoni), emme güçlüğü ve telekardiyografide devasa kardiyomegali saptanıyor. Kan şekeri ölçümleri normal bulunuyor. Biyopside kalp kası lizozomlarının glikojenle tıka basa dolu olduğu görülüyor. Bu hastada eksik olan enzim hangisidir?",
                {
                    "A": "Glukoz-6-fosfataz",
                    "B": "Kas fosforilazı (Miyofosforilaz)",
                    "C": "Lizozomal asit alfa-glukozidaz (asit maltaz)",
                    "D": "Dallanma enzimi",
                    "E": "Karaciğer fosforilazı"
                },
                "C",
                {
                    "A": "Glukoz-6-fosfataz Von Gierke hastalığıdır ve ağır hipoglisemi yapar.",
                    "B": "Kas fosforilazı McArdle hastalığıdır ve erişkinde kramp yapar.",
                    "C": "Doğru! Pompe hastalığında eksik enzim lizozomal asit maltazdır; masif kardiyomegali yapar.",
                    "D": "Dallanma enzimi Andersen hastalığıdır.",
                    "E": "Karaciğer fosforilazı Hers hastalığıdır."
                }
            ),
            make_cloze(
                "Pompe hastalığında glikojenin lizozomlarda parçalanmasından sorumlu olan asit maltaz enzimi eksiktir.",
                "asit maltaz",
                "Pompe hastalığında eksik olan lizozomal hidrolaz"
            )
        ]
    })

    # ADIM 58
    slides.append({
        "slideNumber": 58,
        "title": "Tip V Glikojenoz (McArdle): Kas Fosforilazı ve Egzersiz İntoleransı",
        "subtitle": "Glikolitik ATP yetersizliği, rabdomiyoliz, miyoglobinürik böbrek yetmezliği",
        "badge": "McArdle (Tip V)",
        "badgeColor": "stone",
        "synthesisNarrative": (
            "McArdle hastalığı (Tip V glikojen depo hastalığı), iskelet kasına özgü glikojen fosforilaz (miyofosforilaz) "
            "enziminin kalıtsal eksikliğidir. Karaciğer izoenzimi normal olduğu için kan şekeri dengesi kusursuzdur "
            "ve hepatomegali görülmez. Sorun tamamen iskelet kasının yoğun egzersiz sırasında glikojenden enerji "
            "(ATP) üretememesidir.\n\n"
            "> [SINAV SPOTU] Hastalar yoğun egzersiz sırasında şiddetli ağrılı kas krampları yaşar; kanda laktat "
            "düzeyi yükselmez (çünkü glikoliz çalışamaz). Ağır egzersiz kas membranını yıkarak rabdomiyoliz ve idrarda koyu miyoglobinüri yapar.\n\n"
            "Miyoglobinüri renal tübülleri tıkayarak akut böbrek yetmezliğine yol açabilir."
        ),
        "medicalTerms": [
            {"term": "McArdle Hastalığı (Tip V)", "explanation": "İskelet kası fosforilaz eksikliğinde egzersiz intoleransı ve kramplarla seyreden hastalıktır."},
            {"term": "Rabdomiyoliz", "explanation": "İskelet kas liflerinin parçalanarak miyoglobin ve kreatin kinazın kana dökülmesidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] McArdle hastalığında eksik enzim iskelet kası fosforilazıdır.",
            "📌 [SINAV SPOTU] Egzersiz sonrası kanda laktat artışı olmaması McArdle için tanı koydurucudur."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Doku İzoenzimi", "desc": "Yalnızca iskelet kası tutulur; karaciğer ve kalp etkilenmez.", "isKey": True},
                {"title": "Egzersiz Yanıtı", "desc": "Kramp, rabdomiyoliz, laktat üretememe ve miyoglobinüri.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "Von Gierke (Tip I) vs McArdle (Tip V)",
                "Von Gierke (Tip I - Karaciğer)",
                "G6Paz eksiktir; şiddetli açlık hipoglisemisi, masif hepatomegali ve laktik asidoz ile seyreder.",
                "McArdle (Tip V - İskelet Kası)",
                "Kas fosforilazı eksiktir; kan şekeri ve karaciğer normaldir; egzersiz krampları ve laktat artışı olmaması ile seyreder."
            ),
            make_active_recall(
                "McArdle hastalığında egzersiz testi sırasında kanda laktat düzeyinin yükselmemesinin metabolik sebebi nedir?",
                "Kasta glikojen fosforilaz eksik olduğu için glikojen glukoz-1-fosfata parçalanamaz, glikolize substrat verilemez ve laktat üretilemez."
            )
        ]
    })

    # ADIM 59 - CHECKPOINT 6
    slides.append({
        "slideNumber": 59,
        "title": "[TEKRAR SAYFASI - CHECKPOINT 6] Glikojen Birikimleri ve Depo Hastalıkları",
        "subtitle": "Diyabetik glikojen tutulumu ve Glikojenoz tiplerinin büyük sentezi",
        "badge": "Checkpoint",
        "badgeColor": "red",
        "isCheckpoint": True,
        "checkpointNumber": 6,
        "synthesisNarrative": (
            "Bu checkpoint sayfasında glikojen depolanmalarını ve başlıca glikojen depo hastalıklarını sentezliyoruz. "
            "1) Histokimya: Glikojen PAS(+) boyanır ve amilaz/diyastaz ile sindirildiğinde bu boyanma kaybolur. "
            "2) Diyabette glikojen: Böbrek proksimal tübüllerinde Armanni-Ebstein lezyonu, karaciğerde glikojenli nükleuslar. "
            "3) Von Gierke (Tip I): G6Paz eksikliği, açlık hipoglisemisi, masif hepatomegali. 4) Pompe (Tip II): "
            "Lizozomal asit maltaz eksikliği, masif kardiyomegali, normoglisemi. 5) McArdle (Tip V): Kas fosforilaz "
            "eksikliği, egzersiz krampları, laktat artıramama, miyoglobinüri.\n\n"
            "> [KLİNİK İPUCU] Sınavda kardiyomegali ve bebeklik ölümü Pompe; hipoglisemi ve dev karaciğer Von Gierke; kramp ve koyu idrar McArdle'dır.\n\n"
            "Aşağıdaki 3 akıl kartını dikkatle zihninize sabitleyiniz."
        ),
        "medicalTerms": [
            {"term": "Glikojenoz", "explanation": "Glikojen yıkım enzimlerinin yokluğunda gelişen kalıtsal metabolizma hastalıklarıdır."},
            {"term": "Armanni-Ebstein", "explanation": "Diyabetik ketoasidozda böbrek tübüllerinde glikojen depolanmasıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Pompe = Asit maltaz, kardiyomegali, lizozomal tutulum.",
            "📌 [SINAV SPOTU] Von Gierke = Glukoz-6-fosfataz, açlık hipoglisemisi, hepatomegali.",
            "📌 [SINAV SPOTU] McArdle = Kas fosforilazı, egzersiz krampları, miyoglobinüri."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Diyabet Modeli", "desc": "Armanni-Ebstein tübül hücreleri ve glikojenli nükleus.", "isKey": True},
                {"title": "Tip I (Von Gierke)", "desc": "Hepatik G6Paz defekti, açlık hipoglisemisi.", "isKey": True},
                {"title": "Tip II (Pompe)", "desc": "Lizozomal asit maltaz, dev kardiyomegali.", "isKey": True},
                {"title": "Tip V (McArdle)", "desc": "Kas fosforilazı, egzersiz krampları.", "isKey": True}
            ]
        },
        "flashcards": [
            make_flashcard(
                "k1-07-fc-16",
                "Glikojenin histokimyasal tanısında kullanılan PAS boyası ile diyastaz enziminin ilişkisi nedir?",
                "Glikojen PAS ile pozitif (mor) boyanır; doku önceden diyastaz (amilaz) enzimiyle sindirildiğinde glikojen eridiği için PAS boyanması kaybolur (diyastaza duyarlıdır).",
                "PAS pozitifliği ve diyastaz sindirim testi"
            ),
            make_flashcard(
                "k1-07-fc-17",
                "Armanni-Ebstein lezyonu hangi hastalıkta, hangi organda ve ne birikmesiyle oluşur?",
                "Ağır ve dekompanse diabetes mellitus hastalarında, böbrek proksimal tübül epitel hücrelerinde aşırı glikojen birikmesiyle oluşur.",
                "Diyabetik nefropatide tübüler glikojen lezyonu"
            ),
            make_flashcard(
                "k1-07-fc-18",
                "Pompe hastalığını (Tip II glikojenoz) diğer glikojenozlardan ayıran en temel 2 özellik nedir?",
                "1) Eksik olan enzimin (asit maltaz) lizozomal bir hidrolaz olması, 2) Kan şekeri normal iken masif kardiyomegali ve erken kalp yetmezliği ile seyretmesidir.",
                "Pompe hastalığı enzim lokalizasyonu ve kardiyak tutulum"
            )
        ],
        "interactiveElements": [
            make_cloze(
                "Pompe hastalığında lizozomal enzim eksikliği nedeniyle en ağır harabiyet kalp kası dokusunda gelişir.",
                "kalp kası",
                "Pompe'de aşırı büyüyüp yetmezliğe giren miyokard dokusu"
            )
        ]
    })

    # ADIM 60
    slides.append({
        "slideNumber": 60,
        "title": "Glikojenozlar ve Diyabetik Glikojen Tutulumunun Karşılaştırmalı Sentezi",
        "subtitle": "Klinik senaryolarda glikojen birikimlerinin ayırıcı tanı algoritması",
        "badge": "Klinik Algoritma",
        "badgeColor": "emerald",
        "synthesisNarrative": (
            "Glikojen depolanmasıyla karşılaşan bir hekim, olgunun akkiz metabolik bir bozukluk (diabetes mellitus) mu yoksa "
            "kalıtsal enzim eksikliği (glikojen depo hastalığı) mi olduğunu hızla netleştirmelidir. Diyabette hastanın yaşı "
            "genellikle daha ileri, kan şekeri yüksek ve eşlik eden vasküler bulgular belirgindir.\n\n"
            "> [KLİNİK İPUCU] Glikojenozlar ise çocukluk veya gençlik çağında başlar; karaciğer tutulumunda hipoglisemi, "
            "kas tutulumunda egzersiz krampı, lizozomal tutulumda ise hipotoni ve kardiyomegali ön plandadır.\n\n"
            "Doku biyopsisinde PAS(+) diyastaz duyarlı vakuollerin gösterilmesi ve spesifik enzim düzeylerinin ölçümü "
            "kesin tanıyı koydurur."
        ),
        "medicalTerms": [
            {"term": "Enzim Düzeyi Analizi", "explanation": "Lökosit veya karaciğer/kas biyopsisinde spesifik hidrolaz veya fosforilaz aktivitesinin ölçülmesidir."},
            {"term": "Akkiz vs Kalıtsal", "explanation": "Diyabetin edinsel metabolik dengesizliği ile glikojenozların genetik mutasyon farkıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Diyabette hiperglisemi, karaciğer glikojenozlarında hipoglisemi görülür.",
            "📌 [SINAV SPOTU] Doku biyopsisinde diyastaz testi glikojeni kesinleştirir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Diyabet", "desc": "Kan şekeri yüksek, Armanni-Ebstein tübülleri, glikojenli nükleus.", "isKey": True},
                {"title": "Glikojenoz", "desc": "Kan şekeri düşük veya normal, doku spesifik enzim yokluğu.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_branching_logic(
                "20 yaşında bir üniversite öğrencisi spor salonunda ağırlık kaldırdıktan sonra kollarında şiddetli ağrılı kramplar ve idrarının çay renginde (koyu kahverengi) gelmesi şikayetiyle acile başvuruyor. İdrarda miyoglobin pozitif saptanıyor. Egzersiz testinde kanda laktat artışı izlenmiyor. En olası tanı nedir?",
                [
                    {
                        "text": "Pompe hastalığı: Kalp kasında glikojen birikimi",
                        "isCorrect": False,
                        "feedback": "Pompe hastalığı bebeklikte masif kardiyomegali yapar; egzersiz krampı ve miyoglobinüri yapmaz."
                    },
                    {
                        "text": "McArdle hastalığı (Tip V): İskelet kası fosforilaz eksikliği",
                        "isCorrect": True,
                        "feedback": "Tebrikler! Genç erişkinde egzersizle tetiklenen kramp, laktat üretememe ve miyoglobinüri McArdle hastalığının klasik kliniğidir."
                    }
                ]
            ),
            make_active_recall(
                "Diyabetik ketoasidozdaki glikojen birikimi ile Von Gierke hastalığındaki glikojen birikiminin kan şekeri düzeyleri açısından temel farkı nedir?",
                "Diyabetik ketoasidozda ağır hiperglisemi (yüksek kan şekeri) varken, Von Gierke hastalığında ağır açlık hipoglisemisi (düşük kan şekeri) vardır."
            )
        ]
    })

    return slides
