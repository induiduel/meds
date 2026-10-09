"""
Bölüm 6: Mitokondriyal (İçsel) Yol ve BCL-2 Ailesi
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
        "title": "Apoptozun İki Ana Yolu: İçsel ve Dışsal Yolakların Genel Mimarisi",
        "subtitle": "İndüksiyon ve regülasyonda farklı, ortak kaspaz kaskadında birleşen iki büyük mekanizma",
        "badge": "Yolaklar",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Apoptoz sinyali hücreye iki temel kapıdan girebilir: Hücre içindeki stresi algılayan 'Mitokondriyal "
            "(İçsel) Yol' ve hücre zarındaki ölüm reseptörlerini uyaran 'Ölüm Reseptörü (Dışsal) Yolu'.\n\n"
            "Her iki yol başlangıç sinyalleri, sensör molekülleri ve regülasyon mekanizmaları açısından birbirinden "
            "tamamen farklı olsa da, nihayetinde aynı ortak noktada birleşirler: Başlatıcı kaspazların aktivasyonu "
            "ve ardından ortak infazcı (efektör) kaspazların devreye sokulması!\n\n"
            "> [SINAV SPOTU] Memeli hücrelerinde en sık kullanılan ve fizyolojik/patolojik uyarıların çoğunu "
            "(DNA hasarı, büyüme faktörü yokluğu, ER stresi) yöneten ana yolak 'Mitokondriyal (İçsel) Yol'dur.\n\n"
            "Dışsal yol ise özellikle immün hücrelerin ölüm sinyallerini iletmesinde görev alır."
        ),
        "medicalTerms": [
            {"term": "İçsel (Mitokondriyal) Yol", "explanation": "Hücre içi stres ve hasarı mitokondri membran geçirgenliği üzerinden algılayan apoptoz yolu."},
            {"term": "Dışsal (Ölüm Reseptörü) Yolu", "explanation": "Plazma zarındaki Fas veya TNF reseptörlerinin ligandla uyarılmasıyla başlayan apoptoz yolu."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Apoptozun iki ana yolu vardır: 1) Mitokondriyal (içsel) yol, 2) Ölüm reseptörü (dışsal) yol.",
            "📌 [SINAV SPOTU] İki yol farklı başlatıcılarla başlar ancak ortak kaspaz kaskadında birleşir.",
            "📌 [SINAV SPOTU] Hücre içi stres ve hasarda ana yol Mitokondriyal (içsel) yoldur."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "İki Büyük Kapı", "desc": "İçsel stres (mitokondri) ve dışsal emir (ölüm reseptörleri).", "isKey": True},
                {"title": "Ortak Kaspaz İnfazı", "desc": "Farklı başlatıcıların ortak efektör kaspazlarda kenetlenmesi.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Parametre", "Mitokondriyal (İçsel) Yol", "Ölüm Reseptörü (Dışsal) Yolu"],
                [
                    [("Tetikleyici Faktör", False, ""), ("DNA hasarı, büyüme faktörü kaybı, ER stresi", True, "İntraselüler stres tipleri"), ("FasL, TNF-alfa ligandları", False, "")],
                    [("Kritik Organel / Bölge", False, ""), ("Mitokondri dış zarı geçirgenliği", True, "İçsel yolağın kilit durağı"), ("Plazma zarı ölüm reseptörleri", False, "")],
                    [("Başlatıcı Kaspaz", False, ""), ("Kaspaz-9", True, "İçsel yolun ilk kaspazı"), ("Kaspaz-8 ve Kaspaz-10", False, "")]
                ]
            ),
            make_cloze(
                "Memeli hücrelerinde DNA hasarı ve büyüme faktörü eksikliğinde devreye giren ana apoptoz mekanizması mitokondriyal yoldur.",
                "mitokondriyal",
                "Sitokrom c salınımına dayanan içsel yolak türü"
            )
        ]
    })

    # ADIM 52
    slides.append({
        "slideNumber": 52,
        "title": "BCL-2 Protein Ailesi: Mitokondriyal Kapının Üçlü Bekçileri",
        "subtitle": "Anti-apoptotikler, pro-apoptotik efektörler ve BH3-only stres sensörleri",
        "badge": "BCL-2 Ailesi",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Mitokondriyal yolun kontrol merkezi 'BCL-2 protein ailesi'dir. Bu aile mitokondri dış zarının "
            "geçirgenliğini hassas bir terazi gibi dengeler ve yapısal özelliklerine göre 3 fonksiyonel gruba ayrılır:\n\n"
            "1. Anti-apoptotik Üyeler: BCL-2 ve BCL-XL. Mitokondri zarının sağlamlığını korur, delik açılmasını engeller.\n"
            "2. Pro-apoptotik Efektörler: BAX ve BAK. Mitokondri dış zarında oligomerleşerek kanallar ve porlar açar.\n"
            "3. BH3-only Sensörler: Bad, Bim, Bid, Puma, Noxa. Hücre içi stresi algılayıp BAX/BAK'ı aktive eder.\n\n"
            "> [SINAV SPOTU] Hücrenin yaşayıp öleceğine karar veren nihai denge 'BCL-2/BCL-XL' (koruyucular) ile "
            "'BAX/BAK' (yıkıcılar) arasındaki moleküler orandır!\n\n"
            "Eğer BAX ve BAK üstün gelirse mitokondri dış membranı geçirgenleşir ve geri dönüşsüz apoptoz başlar."
        ),
        "medicalTerms": [
            {"term": "BCL-2 Ailesi", "explanation": "Mitokondri dış membran geçirgenliğini kontrol eden 20'den fazla proteinlik düzenleyici aile."},
            {"term": "BH3-only Proteinler", "explanation": "Yalnızca üçüncü BCL-2 homoloji (BH3) alanını içeren, hücresel stres sensörü proteinler."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Anti-apoptotikler: BCL-2, BCL-XL (mitokondri bütünlüğünü korur).",
            "📌 [SINAV SPOTU] Pro-apoptotik efektörler: BAX, BAK (mitokondri geçirgenliğini artırır, kanal açar).",
            "📌 [SINAV SPOTU] BH3-only sensörler: Bad, Bim, Bid, Puma, Noxa (stres algılar, BAX/BAK'ı uyarır, BCL-2'yi baskılar)."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Anti-apoptotik Kalkan", "desc": "BCL-2 ve BCL-XL'in mitokondri sızıntısını önlemesi.", "isKey": True},
                {"title": "Pro-apoptotik Baltalar", "desc": "BAX ve BAK'ın zarda oligomerik kanallar açması.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Grup Adı", "Aile Üyeleri", "Hücresel / Mitokondriyal Fonksiyonu"],
                [
                    [("Anti-apoptotik Koruyucular", False, ""), ("BCL-2, BCL-XL, MCL-1", True, "Yaşatıcı aile üyeleri"), ("Mitokondri zar bütünlüğünü korur", False, "")],
                    [("Pro-apoptotik Efektörler", False, ""), ("BAX, BAK", True, "Delik açan efektörler"), ("Dış zarda kanal açarak sitokrom c salar", False, "")],
                    [("BH3-only Stres Sensörleri", False, ""), ("Bad, Bim, Bid, Puma, Noxa", True, "Stres algılayıcı öncüler"), ("BAX/BAK'ı aktive eder, BCL-2'yi baskılar", False, "")]
                ]
            ),
            make_cloze(
                "Mitokondri dış zar bütünlüğünü koruyarak apoptoza engel olan temel anti-apoptotik protein BCL-2 proteinidir.",
                "BCL-2",
                "Mitokondriyi sızıntıdan koruyan ana proto-onkogen protein adı"
            )
        ]
    })

    # ADIM 53
    slides.append({
        "slideNumber": 53,
        "title": "Mitokondri Dış Zar Geçirgenleşmesi (MOMP): Sitokrom c Kaçışı",
        "subtitle": "BAX ve BAK oligomerlerinin açtığı porlardan sitoplazmaya dökülen proapoptotik içerik",
        "badge": "MOMP",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Hücrede trofik faktörler azaldığında veya DNA hasarı oluştuğunda BH3-only sensörler hızla aktive olur. "
            "Bu sensörler koruyucu BCL-2 ve BCL-XL'in frenini çözer ve doğrudan BAX ile BAK'a bağlanır.\n\n"
            "Aktive olan BAX ve BAK molekülleri mitokondri dış membranında homooligomerler oluşturarak bir araya gelir. "
            "Bu oligomerler zarda büyük geçirgenlik porları açar; bu olaya 'MOMP' (Mitochondrial Outer Membrane Permeabilization) denir.\n\n"
            "> [SINAV SPOTU] MOMP açıldığında, normalde mitokondrinin zarlar arası aralığında solunum zinciri için "
            "hapsedilmiş olan 'Sitokrom c' kontrolsüzce sitoplazmaya sızar!\n\n"
            "Sitokrom c'nin sitozole sızması, hücre için artık geri dönüşü olmayan infaz hükmünün imzalanması demektir."
        ),
        "medicalTerms": [
            {"term": "MOMP", "explanation": "Mitokondri Dış Membran Geçirgenleşmesi (Mitochondrial Outer Membrane Permeabilization)."},
            {"term": "Sitokrom c", "explanation": "Mitokondri zarlar arası aralıkta elektron taşıyan, sitozole kaçtığında apaptozomu kuran hemoproteini."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] BAX ve BAK dimerleşip kanal oluşturarak mitokondri dış membranını geçirgen hale getirir.",
            "📌 [SINAV SPOTU] Sitokrom c zarlar arası aralıktan sitoplazmaya (sitozole) sızar."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "MOMP Eşiği", "desc": "Bax/Bak oligomerizasyonu ile dış zarın delinmesi.", "isKey": True},
                {"title": "Sitokrom c Firarı", "desc": "Elektron taşıyıcısının sitoplazmaya dökülerek infazı tetiklemesi.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_causal_chain(
                "MOMP ve Sitokrom c Kaçış Mekanizması",
                [
                    "1. Büyüme Faktörü Çekilmesi: Hayatta kalma sinyalleri kesilince BH3-only sensörler aktive olur.",
                    "2. BCL-2 İnhibisyonu: BH3 proteinleri koruyucu BCL-2 ve BCL-XL'i nötralize eder.",
                    "3. BAX/BAK Oligomerizasyonu: Serbest kalan BAX ve BAK mitokondri dış zarında birleşerek por açar.",
                    "4. Zarlar Arası Sızıntı: Dış membran delinir ve mitokondri zarlar arası aralık dışarı açılır.",
                    "5. Sitokrom c Yayılımı: Sitokrom c sitozole taşarak kaspaz kaskadını tetikler."
                ]
            ),
            make_cloze(
                "Mitokondri dış membran geçirgenliğinin artması sonucu zarlar arası aralıktan sitoplazmaya sitokrom c proteini sızar.",
                "sitokrom c",
                "Mitokondriden sitozole sızan kilit proapoptotik hemoproteini"
            )
        ]
    })

    # ADIM 54
    slides.append({
        "slideNumber": 54,
        "title": "Apaptozom Kompleksi: Tekerlek Benzeri Moleküler İnfaz Platformu",
        "subtitle": "Sitokrom c, APAF-1 ve dATP birleşimiyle kurulan heptamerik başlatıcı yapı",
        "badge": "Apaptozom",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Sitoplazmaya firar eden Sitokrom c molekülleri sitozolde tek başına durmaz. Sitokrom c, sitoplazmada "
            "bekleyen 'APAF-1' (Apoptotic Protease Activating Factor-1) adlı adaptör protein ile karşılaşır.\n\n"
            "Sitokrom c'nin APAF-1'e bağlanması ve dATP hidrolizi, APAF-1 proteininin konformasyonunu değiştirerek "
            "7 adet APAF-1/Sitokrom c monomerinin birleşip devasa bir tekerlek (çarkıfelek) benzeri heptamerik "
            "yapı oluşturmasını sağlar. Bu komplekse 'Apaptozom' adı verilir.\n\n"
            "> [SINAV SPOTU] Apaptozomun merkezindeki CARD alanları, inaktif 'Prokaspaz-9' moleküllerini yakalayarak "
            "birbirine yaklaştırır (induced proximity). Böylece 'Başlatıcı Kaspaz-9' aktifleşir!\n\n"
            "Kaspaz-9, mitokondriyal yolağın ilk proteolitik motorudur."
        ),
        "medicalTerms": [
            {"term": "APAF-1", "explanation": "Apoptotik Proteaz Aktive Edici Faktör-1; Sitokrom c bağlayarak apaptozomu kuran adaptör protein."},
            {"term": "Apaptozom", "explanation": "7 adet APAF-1, sitokrom c ve prokaspaz-9'dan oluşan tekerlek biçimli moleküler kaspaz aktivasyon kompleksi."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Sitokrom c sitoplazmada APAF-1 ile birleşerek 'Apaptozom' kompleksini kurar.",
            "📌 [SINAV SPOTU] Apaptozom, mitokondriyal (içsel) yolağın başlatıcı kaspazı olan KASPAZ-9'u aktive eder."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Çarkıfelek Mimarisi", "desc": "7'li APAF-1 ve Sitokrom c heptamerinin kurulması.", "isKey": True},
                {"title": "Kaspaz-9 Aktivasyonu", "desc": "İçsel yolun ilk başlatıcı kaspazının ateşlenmesi.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_micro_quiz(
                "Apoptozun mitokondriyal (içsel) yolunda sitoplazmaya sızan Sitokrom c'nin APAF-1 ile birleşerek oluşturduğu ve Kaspaz-9'u aktive eden kompleks hangisidir?",
                {
                    "A": "İnflamozom",
                    "B": "Apaptozom",
                    "C": "DISC kompleksi",
                    "D": "Splisozom",
                    "E": "Proteazom"
                },
                "B",
                {
                    "A": "İnflamozom piroptozda Kaspaz-1'i aktive eder.",
                    "B": "Doğru cevap B'dir: Sitokrom c + APAF-1 birleşimi Apaptozom kompleksini oluşturur.",
                    "C": "DISC ölüm reseptörü (dışsal) yoluna aittir.",
                    "D": "Splisozom RNA kırpılmasını yapar.",
                    "E": "Proteazom ubikitinlenmiş proteinleri yıkar."
                }
            ),
            make_cloze(
                "Mitokondriyal yolda Sitokrom c sitoplazmada APAF-1 ile birleşerek Kaspaz-9'u aktive eden apaptozom kompleksini kurar.",
                "apaptozom",
                "Sitokrom c ve APAF-1'den oluşan infaz çarkı adı"
            )
        ]
    })

    # ADIM 55
    slides.append({
        "slideNumber": 55,
        "title": "Başlatıcı Kaspaz-9: Mitokondriyal Kaskadın Kıvılcımı",
        "subtitle": "Apaptozom tarafından dimerleştirilip kesilerek aktive edilen içsel yol başlatıcısı",
        "badge": "Kaspaz-9",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Kaspaz ailesi hiyerarşik bir askeri komuta zinciri gibi çalışır. Zincirin tepesinde 'Başlatıcı Kaspazlar' "
            "(initiator caspases), altında ise 'İnfazcı Kaspazlar' (executioner caspases) yer alır.\n\n"
            "Mitokondriyal yolun tek ve tartışmasız başlatıcı kaspazı 'Kaspaz-9'dur. Prokaspaz-9 uzun bir N-terminal "
            "CARD (Caspase Recruitment Domain) prodomaine sahiptir. Apaptozom bu CARD domainleri üzerinden birden fazla "
            "prokaspaz-9'u yan yana getirir.\n\n"
            "> [SINAV SPOTU] Birbirine yaklaşan kaspaz-9 monomerleri oto-proteolitik olarak birbirini keser ve aktif "
            "tetramerik Kaspaz-9 enzimine dönüşür.\n\n"
            "Aktif Kaspaz-9'un tek görevi sitoplazmadaki infazcı prokaspazları (Kaspaz-3 ve Kaspaz-7) bulup onları "
            "keserek zincirleme infazı başlatmaktır."
        ),
        "medicalTerms": [
            {"term": "Başlatıcı Kaspaz (Initiator)", "explanation": "Apoptoz sinyaliyle ilk aktive olan ve efektör kaspazları kesen kaspaz (Kaspaz-8, Kaspaz-9)."},
            {"term": "Kaspaz-9", "explanation": "Apaptozom kompleksi tarafından aktive edilen mitokondriyal (içsel) yol başlatıcı kaspazı."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Mitokondriyal (içsel) yolağın BAŞLATICI kaspazı KASPAZ-9'dur.",
            "📌 [SINAV SPOTU] Kaspaz-9 aktifleşince infazcı kaspazları (özellikle Kaspaz-3) keserek aktive eder."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Hiyerarşik Görev", "desc": "İçsel kaskadın ilk proteolitik kıvılcımını çakma.", "isKey": True},
                {"title": "Efektör Hedefleme", "desc": "Kaspaz-3 ve 7'yi keserek hücreyi yıkıma açma.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_active_recall(
                "Mitokondriyal (içsel) apoptoz yolunun başlatıcı kaspazı hangisidir ve aktivasyonu hangi kompleks üzerinde gerçekleşir?",
                "Başlatıcı kaspaz Kaspaz-9'dur; aktivasyonu Sitokrom c ve APAF-1'in oluşturduğu Apaptozom kompleksi üzerinde gerçekleşir."
            ),
            make_cloze(
                "Apoptozun mitokondriyal yolunda apaptozom kompleksi tarafından aktive edilen başlatıcı kaspaz kaspaz-9 enzimidir.",
                "kaspaz-9",
                "İçsel yolun ilk başlatıcı kaspaz numarası"
            )
        ]
    })

    # ADIM 56
    slides.append({
        "slideNumber": 56,
        "title": "Foliküler Lenfoma ve BCL-2 Onkogeni: t(14;18) Translokasyonu",
        "subtitle": "Anti-apoptotik kalkanın aşırı ekspresyonu ile apoptozdan kaçan B lenfosit tümörü",
        "badge": "Onkoloji",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Apoptozun mitokondriyal yolunun tıptaki en ünlü onkolojik örneği 'Foliküler Lenfoma'dır. B hücreli bir "
            "non-Hodgkin lenfoma olan bu hastalıkta karakteristik bir kromozom translokasyonu saptanır: t(14;18).\n\n"
            "Bu translokasyonda 18. kromozomdaki anti-apoptotik BCL-2 geni, 14. kromozomdaki İmmünoglobulin Ağır Zincir "
            "(IgH) güçlendirici (enhancer) bölgesinin yanına taşınır.\n\n"
            "> [SINAV SPOTU] IgH promotörü B lenfositlerde sürekli aktif olduğundan BCL-2 proteini devasa miktarlarda "
            "aşırı üretilir (overexpression). Aşırı BCL-2 mitokondriyi sızıntıya karşı zırh gibi kapatır!\n\n"
            "Normalde germinal merkezde elenmesi gereken B hücreleri apoptoza gidemez, ölümsüzleşir ve yavaş seyirli "
            "foliküler lenfoma ortaya çıkar. Bu tümör proliferasyon artışıyla değil, apoptoz yetersizliğiyle büyür!"
        ),
        "medicalTerms": [
            {"term": "t(14;18) Translokasyonu", "explanation": "BCL-2 genini IgH enhancer yanına taşıyarak BCL-2 aşırı üretimine yol açan foliküler lenfoma genetik damgası."},
            {"term": "Apoptoz Direnci", "explanation": "Anti-apoptotik BCL-2 fazlalığı nedeniyle tümör hücrelerinin kemoterapiye ve ölüme direnç kazanması."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Foliküler lenfomanın genetik temeli t(14;18) translokasyonudur.",
            "📌 [SINAV SPOTU] t(14;18) sonucu BCL-2 aşırı eksprese olur; apoptoz engellenir ve tümör hücreleri ölümsüzleşir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Translokasyon Mekanizması", "desc": "18q21 (BCL-2) ile 14q32 (IgH) genlerinin kaynaşması.", "isKey": True},
                {"title": "Ölüm Yetersizliği Neoplazisi", "desc": "Mitoz fazlalığı değil, hücre ölümünün durmasıyla gelişen kanser.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_micro_quiz(
                "Aşağıdaki kromozomal translokasyonlardan hangisi anti-apoptotik BCL-2 proteininin aşırı ekspresyonuna yol açarak apoptozu bloke eder ve Foliküler Lenfoma gelişimine neden olur?",
                {
                    "A": "t(9;22) BCR-ABL",
                    "B": "t(8;14) c-MYC",
                    "C": "t(14;18) BCL-2",
                    "D": "t(11;14) Siklin D1",
                    "E": "t(15;17) PML-RARA"
                },
                "C",
                {
                    "A": "t(9;22) KML'deki Ph kromozomudur.",
                    "B": "t(8;14) Burkitt lenfomada c-MYC artışıdır.",
                    "C": "Doğru cevap C'dir: t(14;18) Foliküler lenfomada BCL-2 aşırı üretimi yapar.",
                    "D": "t(11;14) Mantle hücreli lenfomadır.",
                    "E": "t(15;17) Akut promiyelositik lösemidir (APL)."
                }
            ),
            make_cloze(
                "Foliküler lenfomada t(14;18) translokasyonu sonucu anti-apoptotik BCL-2 proteininin aşırı üretimi apoptozu engelleyerek tümöre yol açar.",
                "BCL-2",
                "t(14;18) ile aşırı üretilen anti-apoptotik protein"
            )
        ]
    })

    # ADIM 57
    slides.append({
        "slideNumber": 57,
        "title": "Smac/DIABLO ve IAP İnhibitörleri: İkinci Güvenlik Kilidi",
        "subtitle": "Kaspazları baskılayan IAP proteinlerini etkisizleştiren mitokondriyal müttefikler",
        "badge": "İkinci Kilit",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Hücre içinde kaspaz aktivitesini denetleyen çok katmanlı güvenlik sistemleri mevcuttur. "
            "Sitoplazmada bulunan 'IAP' (Inhibitor of Apoptosis Proteins / Apoptoz İnhibitör Proteinleri), "
            "kazara aktive olmuş kaspazlara (özellikle Kaspaz-3 ve Kaspaz-9) yapışarak onları nötralize eder.\n\n"
            "Ancak hücre gerçek bir apoptoz kararı aldığında mitokondri dış zarından yalnızca Sitokrom c salınmaz.\n\n"
            "> [SINAV SPOTU] Mitokondriden Sitokrom c ile eşzamanlı olarak 'Smac/DIABLO' ve Omi/HtrA2 proteinleri de "
            "sitozole kaçar. Smac/DIABLO gidip sitoplazmik IAP proteinlerine bağlanır ve onları kilitler!\n\n"
            "IAP'lerin kaspazları frenleme gücü kırılınca kaspaz kaskadı tam güçle ve engelsiz şekilde hücresel yıkımı tamamlar."
        ),
        "medicalTerms": [
            {"term": "IAP (Inhibitor of Apoptosis)", "explanation": "Kaspaz-3 ve Kaspaz-9'u doğrudan bağlayıp inhibe eden sitoplazmik güvenlik proteinleri ailesi (örn. XIAP)."},
            {"term": "Smac/DIABLO", "explanation": "Mitokondriden salınarak IAP'leri nötralize eden ve kaspazların önünü açan proapoptotik protein."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Sitoplazmadaki IAP (Apoptoz İnhibitör Proteinleri) kaspazları bloke eder.",
            "📌 [SINAV SPOTU] Mitokondriden sızan Smac/DIABLO, IAP'leri inhibe ederek kaspaz aktivasyonunu serbest bırakır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "IAP Freni", "desc": "Sitoplazmada kaspazların yanlışlıkla patlamasını önleyen bekçiler.", "isKey": True},
                {"title": "Smac/DIABLO İntikamı", "desc": "Mitokondriden çıkıp IAP frenini parçalayan molekül.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "IAP Varlığı vs Smac/DIABLO Salınımı",
                "IAP Etkisi (Hücre Canlı)",
                "Sitoplazmik IAP proteinleri Kaspaz-3 ve 9'u bağlayarak frenler; hafif kaspaz sızıntıları etkisiz kılınır.",
                "Smac/DIABLO Etkisi (Apoptoz)",
                "Mitokondriden sızan Smac/DIABLO IAP'leri kilitler; kaspaz freni kalkar ve tam kaspaz kaskadı patlar."
            ),
            make_cloze(
                "Mitokondriden salınarak sitoplazmadaki apoptoz inhibitör proteinlerini yani IAP'leri bloke eden protein Smac/DIABLO proteinidir.",
                "Smac/DIABLO",
                "IAP'leri nötralize eden mitokondriyal protein adı"
            )
        ]
    })

    # ADIM 58
    slides.append({
        "slideNumber": 58,
        "title": "AIF ve Endonükleaz G: Kaspazdan Bağımsız Mitokondriyal Ölüm",
        "subtitle": "Mitokondriden doğrudan çekirdeğe göç ederek DNA'yı parçalayan infazcılar",
        "badge": "Kaspaz-Bağımsız",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Apoptozun klasik yolu kaspaz kaskadı üzerinden ilerlese de, hücre ölümünün kesinleştiğinden emin "
            "olmak için evrimsel olarak 'Kaspazdan Bağımsız Mitokondriyal Yol' da geliştirilmiştir.\n\n"
            "MOMP gerçekleştiğinde mitokondri zarlar arası aralıktan sitoplazmaya dökülen proteinler arasında "
            "'AIF' (Apoptosis-Inducing Factor) ve 'Endonükleaz G' yer alır.\n\n"
            "> [SINAV SPOTU] AIF ve Endonükleaz G hiçbir kaspaza veya sitozolik aracıya ihtiyaç duymadan doğrudan "
            "hücre çekirdeğine (nükleusa) transloke olurlar. Burada nükleer DNA'yı büyük parçalara keserek "
            "kromatin kondansasyonunu sağlarlar!\n\n"
            "Bu yedek mekanizma sayesinde, tümör hücreleri kaspaz inhibitörleri kullansa dahi mitokondri geçirgenleştiğinde "
            "hücre ölümünden kaçamaz."
        ),
        "medicalTerms": [
            {"term": "AIF (Apoptosis-Inducing Factor)", "explanation": "Mitokondriden nükleusa göç edip kaspazdan bağımsız DNA kırılması ve ölüm yapan protein."},
            {"term": "Endonükleaz G", "explanation": "Mitokondriyal kökenli olup çekirdeğe girerek genomik DNA'yı kesen enzim."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] AIF (Apoptosis-Inducing Factor) ve Endonükleaz G kaspazdan bağımsız apoptozda rol oynar.",
            "📌 [SINAV SPOTU] Mitokondriden çekirdeğe giderek doğrudan DNA parçalanması yaparlar."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Kaspazsız İnfaz", "desc": "Kaspazlar bloke edilse dahi DNA'yı parçalayabilen yedek hat.", "isKey": True},
                {"title": "Nükleer Göç", "desc": "AIF ve Endonükleaz G'nin mitokondriden çekirdeğe sızması.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_active_recall(
                "Mitokondri dış membranı delindiğinde salınan ve hiçbir kaspaza ihtiyaç duymadan doğrudan çekirdeğe gidip DNA'yı parçalayan moleküller nelerdir?",
                "AIF (Apoptosis-Inducing Factor) ve Endonükleaz G'dir."
            ),
            make_cloze(
                "Mitokondriden nükleusa göç ederek kaspazdan bağımsız DNA parçalanmasını gerçekleştiren faktöre AIF veya apoptoz indükleyici faktör denir.",
                "AIF",
                "Kaspaz bağımsız mitokondriyal ölüm faktörü kısaltması"
            )
        ]
    })

    # ADIM 59 (CHECKPOINT 6)
    slides.append({
        "slideNumber": 59,
        "title": "[TEKRAR SAYFASI - CHECKPOINT 6] Mitokondriyal Yol ve BCL-2 Ailesi",
        "subtitle": "BCL-2 terazisi, MOMP, Sitokrom c, Apaptozom, Kaspaz-9 ve foliküler lenfomanın konsolide özeti",
        "badge": "Tekrar Sayfası",
        "badgeColor": "teal",
        "isCheckpoint": True,
        "checkpointNumber": 6,
        "synthesisNarrative": (
            "Bu kontrol noktasında, hücre içi hasarların ana infaz arteri olan Mitokondriyal (İçsel) Apoptoz "
            "yolağını tüm aktörleriyle mühürlüyoruz.\n\n"
            "Süreç BCL-2 ailesinin üçlü dengesiyle yönetilir: Koruyucular (BCL-2, BCL-XL), İnfazcılar (BAX, BAK) "
            "ve Sensörler (BH3-only: Bad, Bim, Bid, Puma, Noxa).\n\n"
            "> [ÖZET REÇETE] Mitokondriyal Yolak Formülü:\n"
            "Stres -> BH3-only aktivasyonu -> BCL-2 baskılanması -> BAX/BAK oligomerizasyonu -> MOMP açılması "
            "-> Sitokrom c sitozole kaçar -> Sitokrom c + APAF-1 = APAPTOZOM -> Başlatıcı KASPAZ-9 aktiflenir "
            "-> Efektör Kaspaz-3 infazı başlatır!\n\n"
            "Foliküler lenfomada t(14;18) translokasyonu BCL-2'yi aşırı üreterek bu kapıyı sonsuza dek kilitler ve tümör oluşturur."
        ),
        "medicalTerms": [
            {"term": "MOMP Eşiği", "explanation": "Mitokondri dış zarının delinerek hücreyi geri dönüşsüz apoptoza soktuğu sınır."},
            {"term": "Kaspaz-9 Tetrameri", "explanation": "Apaptozom üzerinde aktifleşen içsel yol başlatıcı proteazı."}
        ],
        "spotPearls": [
            "📌 [CHECKPOINT ÖZETİ] Anti-apoptotik: BCL-2, BCL-XL. Pro-apoptotik: BAX, BAK. Sensör: BH3-only.",
            "📌 [CHECKPOINT ÖZETİ] MOMP açılınca sitoplazmaya Sitokrom c sızar.",
            "📌 [CHECKPOINT ÖZETİ] Sitokrom c + APAF-1 = Apaptozom -> KASPAZ-9'u aktive eder.",
            "📌 [CHECKPOINT ÖZETİ] t(14;18) foliküler lenfomada BCL-2'yi artırarak apoptozu bloke eder."
        ],
        "flashcards": [
            make_flashcard(
                "fc-k1-05-16",
                "BCL-2 ailesi içerisinde mitokondri dış zarında kanallar açarak geçirgenliği artıran (pro-apoptotik) temel iki efektör protein hangisidir?",
                "BAX ve BAK proteinleridir."
            ),
            make_flashcard(
                "fc-k1-05-17",
                "Mitokondriyal yolda Sitokrom c sitoplazmaya sızdıktan sonra hangi proteinle birleşerek Apaptozomu oluşturur ve hangi kaspazı aktive eder?",
                "APAF-1 ile birleşerek Apaptozom kompleksini kurar ve başlatıcı KASPAZ-9'u aktive eder."
            ),
            make_flashcard(
                "fc-k1-05-18",
                "Foliküler lenfomada görülen karakteristik kromozomal translokasyon ve bunun yol açtığı apoptoz anomalisi nedir?",
                "t(14;18) translokasyonudur; anti-apoptotik BCL-2 proteininin aşırı üretimine ve apoptozun engellenmesine yol açar."
            )
        ],
        "coreContent": {
            "table": {
                "title": "Mitokondriyal Apoptoz Aktörleri Konsolide Tablosu",
                "headers": ["Molekül / Yapı", "Yapısal Konumu", "Apoptozdaki Kritik Rolü"],
                "rows": [
                    ["BCL-2 / BCL-XL", "Mitokondri dış membranı", "Geçirgenliği önler, apoptozu engeller (Anti-apoptotik)"],
                    ["BAX / BAK", "Mitokondri dış membranı", "Oligomerleşip por açar (Pro-apoptotik efektör)"],
                    ["BH3-only (Bim, Puma vb.)", "Sitozol / Hücre iskeleti", "Stres sensörüdür; BAX/BAK'ı uyarır, BCL-2'yi baskılar"],
                    ["Sitokrom c", "Zarlar arası aralık", "Sitozole sızıp APAF-1 ile Apaptozomu kurar"],
                    ["APAF-1", "Sitoplazma", "Sitokrom c ile birleşip çarkıfelek apaptozomu oluşturur"],
                    ["Kaspaz-9", "Apaptozom merkezi", "Mitokondriyal yolağın ilk BAŞLATICI kaspazıdır"],
                    ["Smac/DIABLO", "Mitokondri matriksi", "IAP inhibitörlerini bloke ederek kaspazların önünü açar"]
                ]
            }
        },
        "interactiveElements": [
            make_table(
                ["Apoptoz Basamağı", "Sorumlu Temel Molekül", "İşlevsel Sonuç"],
                [
                    [("Mitokondri Delinmesi", False, ""), ("BAX ve BAK Oligomerleri", True, "Por oluşturan efektörler"), ("MOMP oluşumu ve sitokrom c kaçağı", False, "")],
                    [("Apaptozom Kurulumu", False, ""), ("Sitokrom c + APAF-1", True, "Heptamerik çark bileşenleri"), ("Kaspaz-9'un dimerleşip aktifleşmesi", False, "")],
                    [("Kaspaz Freninin Kırılması", False, ""), ("Smac/DIABLO", True, "Mitokondriyal müttefik"), ("IAP proteinlerinin nötralizasyonu", False, "")]
                ]
            ),
            make_active_recall(
                "Bir kanser ilacı BCL-2 proteinini doğrudan inhibe ederse (örn. Venetoklaks), kanser hücresinde hangi apoptoz basamağı doğrudan tetiklenir?",
                "BAX ve BAK üzerindeki baskı kalkar, mitokondri dış membranı geçirgenleşir (MOMP) ve Sitokrom c salınarak mitokondriyal apoptoz tetiklenir."
            )
        ]
    })

    # ADIM 60
    slides.append({
        "slideNumber": 60,
        "title": "Bcl-2 İnhibitörleri ile Hedefe Yönelik Kanser Tedavisi: Venetoklaks Devrimi",
        "subtitle": "KLL ve AML tedavisinde BH3-mimetik ilaçların mitokondriyal kapağı açması",
        "badge": "Farmakoloji",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Patolojide öğrenilen mitokondriyal apoptoz mekanizması, modern onkolojinin en devrimci ilaç sınıflarından "
            "biri olan 'BH3-mimetiklerin' doğumuna yol açmıştır. Kanser hücreleri (özellikle Kronik Lenfositik Lösemi / KLL "
            "ve Akut Miyeloid Lösemi / AML) hayatta kalabilmek için devasa düzeyde BCL-2 proteini üretir.\n\n"
            "Bu durum mitokondri kapısını sımsıkı kapatır ve kemoterapiye direnç sağlar.\n\n"
            "> [SINAV SPOTU] 'Venetoklaks' (Venetoclax), BCL-2'nin hidrofobik cebine tıpkı endojen bir BH3-only peptit gibi "
            "oturan sentetik küçük bir moleküldür. BCL-2'yi nötralize eder ve BAX/BAK'ı serbest bırakır!\n\n"
            "İlacın verilmesinden birkaç saat sonra lösemi hücreleri kitlesel apoptoza sürüklenir; o kadar hızlı ölürler ki "
            "hastada 'Tümör Lizis Sendromu' gelişmemesi için özel önlemler alınır."
        ),
        "medicalTerms": [
            {"term": "BH3-Mimetik", "explanation": "Endojen BH3-only proteinlerini taklit ederek anti-apoptotik BCL-2'yi bağlayıp felç eden hedefe yönelik ilaç."},
            {"term": "Venetoklaks", "explanation": "BCL-2'yi selektif olarak inhibe eden ve KLL/AML tedavisinde kullanılan FDA onaylı devrimci ilaç."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Venetoklaks BCL-2'yi inhibe eden bir BH3-mimetik moleküldür.",
            "📌 [SINAV SPOTU] KLL ve lösemilerde apoptoz blokajını kırarak kanser hücrelerini mitokondriyal yoldan öldürür."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Hedefe Yönelik Tedavi", "desc": "BCL-2 hidrofobik oluğunun küçük molekülle kapatılması.", "isKey": True},
                {"title": "MOMP Restorasyonu", "desc": "Kanser hücresinde engellenmiş apoptozun yeniden başlatılması.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_branching_logic(
                "Kronik Lenfositik Lösemi (KLL) hastasında BCL-2 aşırı üretimi nedeniyle kemoterapiye direnç gelişmiştir. Onkolog hastaya Venetoklaks başlar. İlacın hücresel etki mekanizması nedir?",
                [
                    {
                        "text": "DNA çift sarmalını çapraz bağlayarak hücreyi nekroza sokar.",
                        "isCorrect": False,
                        "feedback": "Hatalı! Bu klasik alkilleyici kemoterapötiklerin etkisidir."
                    },
                    {
                        "text": "Anti-apoptotik BCL-2'ye bağlanıp onu bloke eder; serbest kalan BAX/BAK mitokondriden sitokrom c salarak apoptozu patlatır.",
                        "isCorrect": True,
                        "feedback": "Kusursuz onkolojik mekanizma! Venetoklaks BCL-2'yi inhibe ederek mitokondriyal apoptozu tetikler."
                    },
                    {
                        "text": "Böbrekten kalsiyum atılımını hızlandırır.",
                        "isCorrect": False,
                        "feedback": "Tıbbi olarak konu dışıdır."
                    }
                ]
            ),
            make_cloze(
                "Lösemi tedavisinde BCL-2 proteinini doğrudan inhibe ederek mitokondriyal apoptozu başlatan hedefe yönelik ilaca Venetoklaks denir.",
                "Venetoklaks",
                "BCL-2 inhibitörü BH3-mimetik ilacın adı"
            )
        ]
    })

    return slides
