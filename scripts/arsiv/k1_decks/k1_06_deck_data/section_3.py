"""
Bölüm 3: Gebelikte Fizyolojik Değişiklikler, Doğum Öncesi Bakım (DÖB) ve David Barker Fetal Programlama Hipotezi
Adımlar: 21 - 30
Checkpoint: Adım 29 (3 Akıl Kartı)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_3_slides():
    slides = []

    # ADIM 21
    slides.append({
        "slideNumber": 21,
        "title": "Gebelikte Maternal Fizyolojik Uyumun Temelleri",
        "subtitle": "Fetüsün büyümesini ve doğumu destekleyen dinamik homeostaz",
        "badge": "Fizyolojik Uyum",
        "badgeColor": "blue",
        "synthesisNarrative": (
            "Gebelik süreci, kadının vücudunda fertilizasyondan doğuma kadar geçen yaklaşık 40 haftalık sürede hemen her "
            "organ sistemini köklü biçimde yeniden yapılandıran olağanüstü bir fizyolojik adaptasyon dönemidir. Bu değişikliklerin "
            "temel gayesi; gelişmekte olan embriyo ve fetüsün besin ve oksijen gereksinimini kesintisiz karşılamak, uteroplasental "
            "dolaşımı beslemek ve anneyi doğum sırasındaki kaçınılmaz kan kaybına karşı korumaktır.\n\n"
            "> [SINAV SPOTU] Gebelikteki fizyolojik değişimler patolojik değildir; ancak sınırları aşıldığında veya yetersiz "
            "kaldığında preeklampsi, gestasyonel diyabet ve anemi gibi komplikasyonlara zemin hazırlar.\n\n"
            "Bu süreçte progesteron, östrojen, insan koryonik gonadotropini (hCG) ve insan plasental laktojeni (hPL) gibi plasental "
            "hormonlar maternal metabolizmayı anabolik fazdan katabolik faza doğru hassas bir dengede yönetir."
        ),
        "medicalTerms": [
            {"term": "Fizyolojik Uyum (Maternal Adaptation)", "explanation": "Gebelikte fetüsü beslemek ve doğuma hazırlanmak için organ sistemlerinde gerçekleşen doğal değişimlerdir."},
            {"term": "İnsan Plasental Laktojeni (hPL)", "explanation": "Maternal insülin direncini artırarak glukozun fetüse geçişini kolaylaştıran plasental hormondur."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Maternal fizyolojik adaptasyon plasental hormonların (özellikle östrojen ve progesteron) orkestrasyonunda gerçekleşir.",
            "📌 [SINAV SPOTU] Değişikliklerin temel hedefi uteroplasental perfüzyonu ve fetal doku oksijenlenmesini güvenceye almaktır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Dinamik Homeostaz", "desc": "Tüm organ sistemleri fetüsün ihtiyaçlarına göre yeniden ayarlanır.", "isKey": True},
                {"title": "Hormonal Kontrol", "desc": "Östrojen, progesteron ve hPL metabolizmayı yönlendirir.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Gebelikte maternal insülin direncini artırarak fetüse glukoz transferini sağlayan temel plasental hormon insan plasental laktojeni molekülüdür.",
                "insan plasental laktojeni",
                "hPL olarak kısaltılan plasenta hormonu"
            ),
            make_active_recall(
                "Gebelikte gerçekleşen multisistemik fizyolojik adaptasyonun iki temel biyolojik amacı nedir?",
                "1. Gelişen fetüse kesintisiz besin ve oksijen sağlamak (uteroplasental perfüzyon), 2. Anneyi doğum eylemindeki fizyolojik kan kaybına ve emzirmeye hazırlamaktır."
            )
        ]
    })

    # ADIM 22
    slides.append({
        "slideNumber": 22,
        "title": "Plazma Hacmi Artışı ve Fizyolojik Hemodilüsyon",
        "subtitle": "Plazma %45-50 artarken eritrositin %20-30 artmasıyla gelişen yalancı anemi",
        "badge": "Hematoloji",
        "badgeColor": "blue",
        "synthesisNarrative": (
            "Gebelikte kan hacminde muazzam bir artış meydana gelir. Maternal plazma hacmi gebelik öncesine göre yaklaşık %45-50 "
            "oranında (yaklaşık 1200-1500 ml) artarken, eritrosit kütlesindeki artış eritropoetin uyarısına rağmen ancak %20-30 "
            "(yaklaşık 300-400 ml) civarında kalır. Sıvı hacmindeki bu orantısız artış, kanda belirgin bir 'fizyolojik hemodilüsyon' "
            "(seyrelme) yaratır.\n\n"
            "> [SINAV SPOTU] Plazma hacmi eritrosit kitlesinden çok daha fazla arttığı için hemoglobin ve hematokrit değerleri fizyolojik "
            "olarak düşer. DSÖ'ye göre gebelikte anemi sınırı Hb < 11 g/dl iken, 2. trimestrde pik hemodilüsyon nedeniyle sınır Hb < 10,5 g/dl kabul edilir.\n\n"
            "Bu fizyolojik seyrelme kan viskozitesini azaltarak maternal vasküler direnci düşürür, mikrosirkülasyonu rahatlatır ve "
            "plasental villuslar arası alanda kanın göllenmesini kolaylaştırarak fetüsün beslenmesini maksimize eder."
        ),
        "medicalTerms": [
            {"term": "Fizyolojik Hemodilüsyon", "explanation": "Plazma hacminin alyuvar kitlesine oranla daha fazla artması sonucu kanın konsantrasyonunun azalmasıdır."},
            {"term": "Gebelik Anemisi Eşiği", "explanation": "1. ve 3. trimestrde Hb < 11 g/dl, 2. trimestrde ise Hb < 10,5 g/dl düzeyidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Plazma hacmi %45-50 artarken alyuvar kütlesi %20-30 artar.",
            "📌 [SINAV SPOTU] Anemi sınırı: 1. ve 3. trimestrde Hb < 11 g/dl, 2. trimestrde Hb < 10,5 g/dl'dir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Plazma %50 Artar", "desc": "Dolaşımdaki sıvı faz hücresel elemanlardan iki kat hızlı büyür.", "isKey": True},
                {"title": "Trimestr Eşikleri", "desc": "İkinci trimestrde pik seyrelme nedeniyle anemi sınırı 10,5 g/dl'ye iner.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Gebelikte ikinci trimestrde pik yapan hemodilüsyon nedeniyle anemi eşiği hemoglobin düzeyi 10,5 g/dl altına indiğinde kabul edilir.",
                "10,5 g/dl",
                "İkinci üç aydaki hemoglobin sınır değeri"
            ),
            make_active_recall(
                "Gebelikte plazma hacmi ile eritrosit kitlesi arasındaki artış oranları nasıldır ve bu durum 2. trimestr anemi sınırını nasıl etkiler?",
                "Plazma hacmi %45-50, eritrosit kitlesi %20-30 artar. Bu orantısız artış (fizyolojik hemodilüsyon) nedeniyle 2. trimestrde anemi sınırı 10,5 g/dl olarak kabul edilir (normalde 11 g/dl)."
            )
        ]
    })

    # ADIM 23
    slides.append({
        "slideNumber": 23,
        "title": "Kardiyovasküler Adaptasyon: Debide Artış ve Vazodilatasyon",
        "subtitle": "Kardiyak debide %30-50 artış, istirahat nabzında yükselme ve üfürümler",
        "badge": "Kardiyoloji",
        "badgeColor": "blue",
        "synthesisNarrative": (
            "Gebelikte kardiyovasküler sistem ağır bir hemodinamik yük altına girer. Kalp debisi (kardiyak output), hem atım hacminin "
            "(stroke volüm) hem de istirahat kalp hızının (dakikada 10-15 atım artış) yükselmesiyle gebelik öncesine göre %30-50 oranında "
            "artar. Bu artışın zirveye ulaştığı dönem 20-24. gebelik haftalarıdır.\n\n"
            "> [SINAV SPOTU] Kardiyak debi %30-50 artmasına rağmen, sistemik vasküler direnç (progesteron ve NO etkisiyle) "
            "belirgin azaldığı için kan basıncı ilk iki trimestrde fizyolojik olarak DÜŞER (diyastolik 5-10 mmHg azalır).\n\n"
            "Artan debi ve kan akım hızına bağlı olarak gebelerin %90'ından fazlasında fizyolojik sistolik ejeksiyon üfürümü duyulur. "
            "Üçüncü trimestrde büyüyen uterusun vena cava inferiora bası yapmasıyla supin hipotansif sendrom gelişebilir."
        ),
        "medicalTerms": [
            {"term": "Kardiyak Debi Artışı", "explanation": "Dakikada pompalanan kan miktarının 4,5 L'den yaklaşık 6-7 L'ye çıkmasıdır."},
            {"term": "Supin Hipotansif Sendrom", "explanation": "Sırtüstü yatan gebede uterusun vena kavaya basarak venöz dönüşü ve tansiyonu düşürmesidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Gebelikte kardiyak debi %30-50 artar; zirve noktası 20-24. haftalardır.",
            "📌 [SINAV SPOTU] Progesteron ve nitrik oksit damarları genişletir; erken gebelikte tansiyon fizyolojik olarak düşer."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Debi %30-50 Artar", "desc": "Uteroplasental ve renal perfüzyonu beslemek için kalp debisi yükselir.", "isKey": True},
                {"title": "Vazodilatasyon", "desc": "Periferik direnç düşerek kan basıncını erken haftalarda aşağı çeker.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Sırtüstü yatan gebede uterusun vena cava inferiora bası yapmasıyla venöz dönüşün azalıp bayılma hissi oluşmasına supin hipotansif sendrom denir.",
                "supin hipotansif sendrom",
                "Sırtüstü yatışta gelişen tansiyon düşmesi"
            ),
            make_active_recall(
                "Gebelikte kardiyak debi %30-50 artmasına rağmen kan basıncının ilk iki trimestrde düşmesinin mekanizması nedir?",
                "Progesteron, nitrik oksit ve prostasiklin etkisiyle düz kasların gevşemesi ve sistemik vasküler direncin (afterload) belirgin şekilde azalmasıdır."
            )
        ]
    })

    # ADIM 24
    slides.append({
        "slideNumber": 24,
        "title": "Solunum Sistemi: Oksijen İhtiyacında %20-30 Artış",
        "subtitle": "Dakika ventilasyonunda artış, progesterona bağlı hiperventilasyon ve solunumsal alkaloz",
        "badge": "Solunum",
        "badgeColor": "blue",
        "synthesisNarrative": (
            "Fetüsün ve plasentanın büyümesi, maternal dokuların genişlemesi ve kardiyak iş yükünün artması sonucunda maternal "
            "oksijen tüketimi gebelik boyunca %20 ila %30 oranında artış gösterir. Bu devasa oksijen açığını kapatmak üzere solunum "
            "sistemi progesteron hormonunun doğrudan meduller solunum merkezini uyarmasıyla dakika ventilasyonunu %40-50 artırır.\n\n"
            "> [SINAV SPOTU] Gebelikte oksijen ihtiyacı %20-30 artar. Solunum sayısı (frekansı) belirgin değişmezken, tidal volüm "
            "(derinlik) artar; bu durum fizyolojik kompanse solunumsal alkaloza (pCO2 ~ 28-32 mmHg) yol açar.\n\n"
            "Maternal kanda pCO2'nin düşmesi, fetal kandan maternal kana karbondioksit geçişini (Bohr etkisi) dramatik olarak kolaylaştırır. "
            "Uterusun diyaframı 4 cm yukarı itmesi rezidüel hacmi azaltsa da toraks çevre genişlemesi ile total akciğer kapasitesi korunur."
        ),
        "medicalTerms": [
            {"term": "Tidal Volüm Artışı", "explanation": "Her nefeste alınan hava miktarının 500 ml'den yaklaşık 700 ml'ye çıkmasıdır."},
            {"term": "Kompanse Solunumsal Alkaloz", "explanation": "Progesteronun tetiklediği hiperventilasyonla pCO2'nin 30 mmHg civarına inmesi ve böbreklerin bikarbonat atmasıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Gebelikte oksijen gereksinimi %20-30 oranında artar.",
            "📌 [SINAV SPOTU] Dakika ventilasyonu tidal volüm artışıyla sağlanır; hafif kompanse solunumsal alkaloz fizyolojiktir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "%20-30 O2 Artışı", "desc": "Fetal metabolizma ve maternal organlar için oksijen tüketimi tırmanır.", "isKey": True},
                {"title": "Progesteron Uyarısı", "desc": "Solunum merkezini uyararak tidal hacmi artırır ve pCO2'yi düşürür.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Gebelikte fetüs ve anne dokularının metabolik gereksinimi nedeniyle maternal oksijen ihtiyacında yüzde 20-30 artış meydana gelir.",
                "yüzde 20-30",
                "Oksijen tüketimindeki artış yüzdesi"
            ),
            make_active_recall(
                "Gebelikte artan dakika ventilasyonu ve pCO2'nin düşmesi (fizyolojik solunumsal alkaloz) fetüse gaz değişiminde nasıl bir avantaj sağlar?",
                "Maternal kanda pCO2 düştüğünde maternal-fetal CO2 gradyenti artar; fetüsün metabolik atığı olan karbondioksit plasentadan anne kanına hızla difüze olur."
            )
        ]
    })

    # ADIM 25
    slides.append({
        "slideNumber": 25,
        "title": "Gastrointestinal Sistem: Progesteronun Düz Kas Gevşetici Etkisi",
        "subtitle": "Mide boşalmasında gecikme, reflü, konstipasyon ve safra stazı",
        "badge": "Gastrointestinal",
        "badgeColor": "blue",
        "synthesisNarrative": (
            "Gebelikte yüksek düzeyde salgılanan progesteron hormonu, vücuttaki tüm düz kas lifleri üzerinde belirgin bir gevşetici "
            "(relaksasyon) ve motiliteyi baskılayıcı etki gösterir. Bu etkinin gastrointestinal sistemdeki yansıması; alt özofagus "
            "sfinkter tonusunun düşmesi (gastroözofageal reflü ve pirozis), mide ve bağırsak pasajının uzaması ve kolonik su emiliminin "
            "artmasıyla ortaya çıkan inatçı konstipasyondur (kabızlık).\n\n"
            "> [SINAV SPOTU] Progesteron etkisiyle safra kesesi motilitesi azalır, safra stazı ve kolesterol doygunluğu artar; "
            "bu durum gebelikte safra taşı (kolelitiyazis) ve intrahepatik kolestaz riskini belirgin yükseltir.\n\n"
            "Bağırsak transit süresinin uzaması olumsuz görünse de, fizyolojik açıdan kalsiyum, demir ve diğer mikrobesinlerin bağırsak "
            "mukozasıyla temas süresini uzatarak emilim verimliliğini artıran adaptif bir amaca da hizmet eder."
        ),
        "medicalTerms": [
            {"term": "Safra Stazı", "explanation": "Progesteronun safra kesesi kontraksiyonunu yavaşlatması sonucu safranın durağanlaşmasıdır."},
            {"term": "Gastroözofageal Reflü (Pirozis)", "explanation": "Gevşeyen alt özofagus sfinkterinden asit içeriğin yemek borusuna kaçarak göğüste yanma yapmasıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Progesteron düz kasları gevşeterek reflü, konstipasyon ve safra stazına zemin hazırlar.",
            "📌 [SINAV SPOTU] Bağırsak geçişinin yavaşlaması besin ve minerallerin emilim süresini uzatır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Düz Kas Gevşemesi", "desc": "Progesteron motiliteyi yavaşlatarak sfinkterleri gevşetir.", "isKey": True},
                {"title": "Safra Taşı Riski", "desc": "Kesenin boşalamaması kolesterol kristalleşmesine yol açar.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Gebelikte progesteron etkisiyle safra kesesinin boşalmasının gecikmesi ve safranın göllenmesi tablosuna safra stazı denir.",
                "safra stazı",
                "Kese motilitesinin duraklaması"
            ),
            make_active_recall(
                "Progesteron hormonunun gastrointestinal sistem düz kaslarını gevşetmesinin yol açtığı üç tipik klinik sorun nedir?",
                "1. Gastroözofageal reflü (mide yanması), 2. Konstipasyon (kabızlık), 3. Safra kesesi motilite azalması ve safra stazı (taş eğilimi)."
            )
        ]
    })

    # ADIM 26
    slides.append({
        "slideNumber": 26,
        "title": "Doğum Öncesi Bakım (DÖB): Tanım, Amaç ve İzlem Standartları",
        "subtitle": "Eğitilmiş sağlık personeli eşliğinde periyodik kontrol ve risk taraması",
        "badge": "Doğum Öncesi Bakım",
        "badgeColor": "emerald",
        "synthesisNarrative": (
            "Doğum Öncesi Bakım (DÖB); anne ve karnındaki bebeğin gebelik süresince düzenli aralıklarla, eğitilmiş ve vasıflı bir "
            "sağlık personeli (ebe veya hekim) tarafından muayene edilmesi, olası risk faktörlerinin erkenden saptanması, gerekli "
            "profilaktik desteklerin sunulması ve tavsiyelerde bulunulması sürecidir.\n\n"
            "> [SINAV SPOTU] DSÖ kılavuzlarına göre olumlu bir gebelik deneyimi ve komplikasyonların önlenmesi için gebelik boyunca "
            "EN AZ 8 KEZ sağlık personeli ile yüz yüze DÖB viziti önerilmektedir (Türkiye Sağlık Bakanlığı asgari 4 izlem şart koşar).\n\n"
            "DÖB yalnızca tansiyon ölçümü veya ultrasonografi değildir; anemi taraması, idrar proteini incelemesi, tetanoz aşısı, "
            "demir-D vitamini desteği ve doğum planının yapılmasını içeren kapsamlı bir koruyucu halk sağlığı paketidir."
        ),
        "medicalTerms": [
            {"term": "Doğum Öncesi Bakım (Antenatal Care - ANC)", "explanation": "Gebelik sürecinde anne ve fetüsün sağlığını korumak amacıyla yürütülen standart izlem programıdır."},
            {"term": "Asgari DÖB Viziti", "explanation": "DSÖ'nün güncel kılavuzunda önerdiği en az 8 temaslı izlem modelidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Doğum öncesi bakım: Anne ve bebeğin periyodik muayene, tarama ve danışmanlıkla izlenmesidir.",
            "📌 [SINAV SPOTU] DSÖ en az 8 izlem temasını hedeflerken, Sağlık Bakanlığı protokolü asgari 4 nitelikli izlemi zorunlu tutar."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Periyodik İzlem", "desc": "Gebelikte tansiyon, kilo, proteinüri ve fetal büyüme düzenli taranır.", "isKey": True},
                {"title": "Erken Teşhis", "desc": "Preeklampsi ve gestasyonel diyabet semptomsuz dönemde yakalanır.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Dünya Sağlık Örgütü olumlu bir gebelik süreci için gebelik boyunca en az 8 temas içeren doğum öncesi bakım önermektedir.",
                "doğum öncesi bakım",
                "Gebelikte sunulan periyodik koruyucu izlem hizmeti"
            ),
            make_active_recall(
                "Doğum öncesi bakımın (DÖB) temel felsefesi nedir ve rutin bir vizitte hangi temel taramalar mutlaka yapılır?",
                "Anne ve bebeği periyodik muayenelerle izleyip riskleri erkenden saptamaktır. Rutin vizitte kan basıncı, kilo takibi, idrarda proteinüri, anemi taraması ve fetal kalp sesleri değerlendirilir."
            )
        ]
    })

    # ADIM 27
    slides.append({
        "slideNumber": 27,
        "title": "DÖB İçeriği: Danışmanlık ve Tehlike İşaretleri Eğitimi",
        "subtitle": "Kişisel hijyen, beslenme, zararlı maddeler ve acil obstetrik belirtiler",
        "badge": "Eğitim ve Danışmanlık",
        "badgeColor": "emerald",
        "synthesisNarrative": (
            "Nitelikli bir doğum öncesi bakım vizitinin en kritik bileşenlerinden biri anne adayına verilen yapılandırılmış sağlık "
            "eğitimidir. Bu eğitim; dengeli beslenme ilkeleri, kilo kontrolü, kişisel ve dental hijyen, gebelikte güvenli fiziksel "
            "aktivite, sigara, alkol ve toksik maddelerin kesin zararları ile sık görülen gebelik yakınmalarının yönetimini kapsar.\n\n"
            "> [SINAV SPOTU] DÖB eğitiminin hayati parçası 'Obstetrik Tehlike İşaretleri'dir: Vajinal kanama, konvülsiyon, şiddetli baş "
            "ağrısı/bulanık görme, yüksek ateş, su gelmesi ve fetal hareketlerde azalma derhal hastaneye başvuruyu gerektirir.\n\n"
            "Annenin bu belirtileri öğrenmesi, Üç Gecikme Modeli'nin ilk basamağı olan 'bakım aramaya karar verme gecikmesini' ortadan "
            "kaldırarak hayat kurtarır."
        ),
        "medicalTerms": [
            {"term": "Obstetrik Tehlike İşaretleri", "explanation": "Gebelikte acil cerrahi veya medikal müdahale gerektiren hayati alarm semptomlarıdır."},
            {"term": "Fetal Hareket Sayımı", "explanation": "Üçüncü trimestrde fetal iyilik halini gösteren annenin günlük bebek tekmelerini izleme testidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] DÖB eğitimi: Hijyen, beslenme, madde bağımlılığı önleme ve tehlike işaretlerini öğretmeyi kapsar.",
            "📌 [SINAV SPOTU] Kanama, şiddetli baş ağrısı, su gelmesi ve bebek hareketlerinin durması majör tehlike işaretleridir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Farkındalık Gücü", "desc": "Eğitilen anne tehlike işaretini anında fark edip hastaneye koşar.", "isKey": True},
                {"title": "Zararlı Alışkanlıklar", "desc": "Sigara ve alkolün teratojenik etkileri açıkça anlatılır.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Doğum öncesi bakımda gebeye öğretilen vajinal kanama ve şiddetli baş ağrısı gibi bulgulara obstetrik tehlike işaretleri adı verilir.",
                "obstetrik tehlike işaretleri",
                "Acil hastaneye gitmeyi gerektiren alarm semptomları"
            ),
            make_active_recall(
                "Bir gebenin acilen tam teşekküllü bir hastaneye başvurmasını gerektiren başlıca obstetrik tehlike işaretleri nelerdir?",
                "Vajinal kanama, şiddetli baş ağrısı ve görme bulanıklığı (preeklampsi öncülü), vajinadan sıvı gelmesi (membran rüptürü), yüksek ateş ve fetal hareketlerin hissedilmemesidir."
            )
        ]
    })

    # ADIM 28
    slides.append({
        "slideNumber": 28,
        "title": "Fetal Programlama ve David Barker Hipotezi",
        "subtitle": "İntrauterin malnütrisyonun erişkin yaşta koroner kalp hastalığı mirası",
        "badge": "Barker Hipotezi",
        "badgeColor": "purple",
        "synthesisNarrative": (
            "İngiliz epidemiyolog David Barker tarafından 1980'lerin sonunda ortaya atılan 'Fetal Programlama Hipotezi' (Barker Hipotezi "
            "veya DOHaD - Developmental Origins of Health and Disease), anne karnındaki fetal çevrenin bireyin tüm yetişkinlik yaşamındaki "
            "kronik hastalık riskini kalıcı olarak biçimlendirdiğini savunur.\n\n"
            "> [SINAV SPOTU] Fetal Programlama Hipotezi'ni tıp literatürüne kazandıran bilim insanı DAVID BARKER'dır. Hipoteze göre "
            "intrauterin dönemdeki yetersiz beslenme, erişkin çağda Tip 2 Diyabet, Hipertansiyon ve Koroner Arter Hastalığı riskini katlar.\n\n"
            "Fetüs, rahim içinde besin ve oksijen yetersizliği ile karşılaştığında hayatta kalabilmek için sınırlı kaynakları beyin "
            "gibi hayati organlara yönlendirir (brain sparing). Bu esnada pankreas beta adacıkları, nefron sayısı ve karaciğer fonksiyonları "
            "kısıtlanır; gen ifadesi 'kıtlık koşullarına' göre kalıcı olarak programlanır."
        ),
        "medicalTerms": [
            {"term": "David Barker Hipotezi", "explanation": "İntrauterin beslenme yetersizliğinin erişkin başlangıçlı kardiyovasküler ve metabolik hastalıkların kökenini oluşturduğunu açıklayan teoridir."},
            {"term": "DOHaD", "explanation": "Sağlık ve Hastalığın Gelişimsel Kökenleri (Developmental Origins of Health and Disease) disiplinidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Fetal programlama hipotezinin öncüsü David Barker'dır.",
            "📌 [SINAV SPOTU] İntrauterin malnütrisyon erişkinlikte koroner arter hastalığı, inme ve tip 2 diyabet riskini dramatik artırır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "David Barker", "desc": "Gebelikte maternal beslenmenin erişkin sağlığına etkisini kanıtlayan öncüdür.", "isKey": True},
                {"title": "Kalıcı Programlama", "desc": "İntrauterin kıtlık metabolik organların yapısını ve fonksiyonunu kısıtlar.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Fetal dönemde maruz kalınan olumsuz ortamın erişkin kronik hastalıklarıyla ilişkisini açıklayan hipotezin kurucusu David Barker olarak bilinir.",
                "David Barker",
                "Fetal programlama hipotezini kuran araştırmacı"
            ),
            make_active_recall(
                "David Barker Hipotezi'nin (Fetal Programlama) temel önermesi nedir ve intrauterin yetersiz beslenme erişkinlikte hangi hastalıklara zemin hazırlar?",
                "Temel önerme: Fetal dönemdeki maternal beslenme ortamı erişkin sağlığını kalıcı olarak biçimlendirir. İntrauterin malnütrisyon erişkinlikte koroner kalp hastalığı, hipertansiyon, Tip 2 diyabet ve metabolik sendrom riskini artırır."
            )
        ]
    })

    # ADIM 29 [CHECKPOINT 3]
    slides.append({
        "slideNumber": 29,
        "title": "[TEKRAR SAYFASI - CHECKPOINT 3] Fizyolojik Değişiklikler ve Barker Hipotezi İstasyonu",
        "subtitle": "Hemodilüsyon, solunum adaptasyonu, DÖB ve fetal programlamanın sentezi",
        "badge": "Checkpoint",
        "badgeColor": "teal",
        "isCheckpoint": True,
        "checkpointNumber": 3,
        "synthesisNarrative": (
            "Bu istasyon; gebelikte plazma hacminin %45-50, eritrositin %20-30 artmasıyla oluşan fizyolojik hemodilüsyonu (2. trimestr "
            "anemi sınırı 10,5 g/dl), kardiyak debide %30-50 artışı, oksijen tüketiminde %20-30 yükselişi ve progesterona bağlı hafif "
            "kompanse solunumsal alkalozu, gastrointestinal sistemde sfinkter gevşemesi ve safra stazını, Doğum Öncesi Bakımın (DÖB) "
            "koruyucu gücünü ve David Barker'ın Fetal Programlama Hipotezi'ni konsolide eder.\n\n"
            "> [YÜKSEK VERİM] Hb < 10,5 g/dl (2. trimestr); O2 ihtiyacı +%20-30; Progesteron = düz kas gevşemesi; DÖB = en az 8 vizit "
            "(DSÖ); David Barker = intrauterin malnütrisyon → erişkin KAH ve diyabet."
        ),
        "medicalTerms": [
            {"term": "Hemodilüsyon Dinamiği", "explanation": "Plazma artışının eritrositi aşması sonucu viskozitenin düşmesidir."},
            {"term": "Fetal Programlama Triadı", "explanation": "İntrauterin kıtlık, düşük doğum ağırlığı ve erişkin metabolik sendromdur."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Plazma %50, eritrosit %20-30 artar -> Fizyolojik hemodilüsyon (2. trimestr Hb < 10,5 g/dl anemi).",
            "📌 [SINAV SPOTU] Oksijen gereksinimi %20-30 artar; dakika solunumu tidal volüm artışıyla kompanse edilir.",
            "📌 [SINAV SPOTU] David Barker: İntrauterin ortam yetişkinlikte koroner kalp hastalığı ve diyabeti programlar."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Hemodilüsyon", "desc": "Viskozite azalır, plasental kanlanma kolaylaşır.", "isKey": True},
                {"title": "DÖB Önemi", "desc": "Riskleri erkenden yakalayarak maternal ölümü engeller.", "isKey": True},
                {"title": "Barker İlkesi", "desc": "Anne karnındaki beslenme erişkin sağlığının kaderini çizer.", "isKey": True}
            ]
        },
        "flashcards": [
            make_flashcard(
                "fc-k1-06-07",
                "Gebelikte plazma hacmi ve alyuvar kitlesi artış oranları nasıldır ve 2. trimestr anemi sınırı kaçtır?",
                "Plazma hacmi %45-50, alyuvar kitlesi %20-30 artar. Bu fizyolojik hemodilüsyon nedeniyle 2. trimestrde anemi eşiği Hb < 10,5 g/dl'dir.",
                "Hemodilüsyon ve 10,5 g/dl"
            ),
            make_flashcard(
                "fc-k1-06-08",
                "Gebelikte oksijen tüketimi ne oranda artar ve solunum sistemi bu gereksinimi nasıl karşılar?",
                "Oksijen tüketimi %20-30 oranında artar; solunum hızı değişmezken progesteron uyarısıyla tidal volüm artarak dakika solunumu yükseltilir.",
                "Oksijen %20-30 ve tidal hacim"
            ),
            make_flashcard(
                "fc-k1-06-09",
                "Fetal Programlama Hipotezi kim tarafından kurulmuştur ve ana mesajı nedir?",
                "David Barker tarafından kurulmuştur; fetal dönemdeki beslenme yetersizliği yetişkinlikte KAH, hipertansiyon ve Tip 2 diyabet riskini kalıcı olarak artırır.",
                "David Barker hipotezi"
            )
        ],
        "interactiveElements": [
            make_table(
                ["Fizyolojik Parametre", "Gebelikteki Değişim Yönü / Oranı", "Klinik Yansıması / Önemi"],
                [
                    [("Plazma Hacmi", False, ""), ("Yüzde 45-50 oranında artış", True, "Sıvı fazdaki devasa yükselme"), ("Fizyolojik hemodilüsyon ve viskozite düşüşü", False, "")],
                    [("Oksijen Tüketimi", False, ""), ("Yüzde 20-30 oranında artış", True, "Metabolik oksijen talebi artışı"), ("Progesterona bağlı hiperventilasyon ve alkaloz", False, "")],
                    [("Gastrointestinal Motilite", False, ""), ("Progesteron ile belirgin yavaşlama", False, ""), ("Gastroözofageal reflü ve safra stazı", True, "Düz kas gevşemesine bağlı klinik yakınma")]
                ]
            )
        ]
    })

    # ADIM 30
    slides.append({
        "slideNumber": 30,
        "title": "Tasarruflu Fenotip Hipotezi (Thrifty Phenotype): Moleküler Köprü",
        "subtitle": "Hales ve Barker'ın glukoz intoleransı ve adipozite modeli",
        "badge": "Tasarruflu Fenotip",
        "badgeColor": "purple",
        "synthesisNarrative": (
            "David Barker ve Nick Hales tarafından geliştirilen 'Tasarruflu Fenotip Hipotezi' (Thrifty Phenotype Hypothesis), "
            "fetal programlamanın moleküler ve metabolik mantığını açıklar. Anne karnında yetersiz glukoz ve aminoasit alan fetüs, "
            "metabolik ayarlarını kalıcı olarak 'kıtlık ortamına' uyarlar; dokularda insülin direnci geliştirerek glukozu beyne yönlendirir "
            "ve her kaloriyi maksimum verimle yağ dokusunda depolamaya programlanır.\n\n"
            "> [SINAV SPOTU] Tasarruflu fenotip geliştiren düşük doğum ağırlıklı bebek, doğumdan sonra bol kalorili ve hareketsiz "
            "bir çevreyle karşılaştığında ('mismatch' - uyumsuzluk), hızla santral obezite, insülin direnci ve Tip 2 diyabete sürüklenir.\n\n"
            "Epigenetik düzeyde DNA metilasyonu ve histon modifikasyonları yoluyla gerçekleşen bu programlama, anne karnındaki 9 ayın "
            "gelecek 70 yıllık yaşam beklentisini nasıl ipotek altına aldığını gösterir."
        ),
        "medicalTerms": [
            {"term": "Tasarruflu Fenotip (Thrifty Phenotype)", "explanation": "İntrauterin malnütrisyona yanıt olarak enerjiyi depolamaya ve insüline direnmeye programlanmış metabolizmadır."},
            {"term": "Metabolik Uyumsuzluk (Mismatch)", "explanation": "Fetal dönemdeki kıtlık programı ile doğum sonrasındaki aşırı kalorili batı tipi beslenme arasındaki çatışmadır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Hales ve Barker'ın tasarruflu fenotip hipotezi düşük doğum ağırlığının Tip 2 diyabet riskini nasıl artırdığını açıklar.",
            "📌 [SINAV SPOTU] Fetal kıtlık programı doğum sonrası bolluk ortamıyla çatıştığında metabolik sendrom patlak verir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Kıtlığa Adaptasyon", "desc": "Fetüs hayatta kalmak için metabolizmasını düşük enerjiye kilitler.", "isKey": True},
                {"title": "Bolluk Çatışması", "desc": "Doğum sonrası zengin diyet organları hızla iflasa ve diyabete götürür.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "İntrauterin yetersiz beslenmeye karşı fetüsün enerjiyi depolamaya odaklı kalıcı adaptasyonuna tasarruflu fenotip hipotezi denir.",
                "tasarruflu fenotip",
                "Hales ve Barker'ın metabolik uyum modeli"
            ),
            make_active_recall(
                "Tasarruflu Fenotip Hipotezi'ne göre düşük doğum ağırlıklı doğan bir bebeğin erişkinlikte Tip 2 diyabete yakalanma riski neden yüksektir?",
                "Fetüs rahim içindeki yetersiz besin ortamında glukozu korumak için periferik dokularda kalıcı insülin direnci geliştirir. Doğum sonrası zengin kalorili beslendiğinde bu tasarruflu ayarlar hızla dekompanse olarak diyabete yol açar."
            )
        ]
    })

    return slides
