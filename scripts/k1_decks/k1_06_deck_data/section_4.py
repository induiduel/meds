"""
Bölüm 4: Maternal Malnütrisyon ve Aşırı Beslenmenin Maternal-Fetal Sonuçları, Riskli Gebelik Kriterleri
Adımlar: 31 - 40
Checkpoint: Adım 39 (3 Akıl Kartı)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_4_slides():
    slides = []

    # ADIM 31
    slides.append({
        "slideNumber": 31,
        "title": "Gebelikte Beslenmenin 4 Temel Amacı ve 'İki Canlı' Yanılgısı",
        "subtitle": "Kendi gereksinimi, depoların korunması, fetal gelişim ve emzirme hazırlığı",
        "badge": "Beslenme İlkeleri",
        "badgeColor": "emerald",
        "synthesisNarrative": (
            "Gebelikte dengeli ve yeterli beslenme, rastgele bir kalori artışı değil; dört hayati biyolojik hedefe hizmet eden "
            "hassas bir planlamadır: 1) Annenin kendi artan fizyolojik gereksinimlerini karşılamak, 2) Annenin vücut besin depolarını "
            "tükenmekten koruyup dengede tutmak, 3) Bebeğin intrauterin büyüme, organogenez ve gelişimini eksiksiz sağlamak ve "
            "4) Doğum sonrası emzirme döneminde salgılanacak anne sütünün enerji ve besin ögelerini depolamak.\n\n"
            "> [SINAV SPOTU] Halk arasında yaygın olan 'gebe kadın iki canlıdır, her şeyden iki kat yemelidir' anlayışı tamamen "
            "yanlış ve tehlikelidir; doğru olan her şeyden iki misli yemek değil, bazı besin ögelerinden belirli miktarda fazla tüketmektir.\n\n"
            "Kontrolsüz kalori alımı kadında aşırı kilo kazanımı, gestasyonel diyabet ve makrozomiye zemin hazırlarken, niteliksiz "
            "beslenme ise kaloriye rağmen mikrobesin eksiklikleri (gizli açlık) doğurur."
        ),
        "medicalTerms": [
            {"term": "Gizli Açlık (Hidden Hunger)", "explanation": "Yeterli kalori alınmasına rağmen vitamin ve mineral gibi elzem mikrobesinlerin eksik olması durumudur."},
            {"term": "Gebelikte Depo Yağ", "explanation": "Emzirme döneminde süt sentezi için 3. trimestrde depolanan yaklaşık 3-4 kg'lık maternal fizyolojik yağ dokusudur."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Beslenmenin 4 amacı: Annenin gereksinimi, depoların korunması, fetal gelişim ve süt sentezi hazırlığıdır.",
            "📌 [SINAV SPOTU] 'İki canlı' diye iki kat yemek yanlıştır; belirli besin ögelerinden (protein, demir, kalsiyum vb.) hedefe yönelik artış gerekir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "4 Stratejik Amaç", "desc": "Anne, bebek, depolar ve süt salgısı dengesi kurulur.", "isKey": True},
                {"title": "İki Canlı Yanılgısı", "desc": "Çift porsiyon yemek obezite ve gestasyonel diyabet tuzağıdır.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Gebelikte her şeyden iki kat yemek yerine belirli besin öğelerinden hedeflenen miktarda fazla tüketmek esastır.",
                "belirli besin öğelerinden",
                "Beslenme stratejisindeki seçici yaklaşım"
            ),
            make_active_recall(
                "Gebelikte yeterli ve dengeli beslenmenin hizmet ettiği 4 temel fizyolojik amaç nelerdir?",
                "1. Annenin kendi metabolik gereksinimlerini karşılamak, 2. Maternal depoları korumak, 3. Bebeğin optimal büyüme-gelişmesini sağlamak, 4. Emzirme döneminde süt üretimi için enerji ve besin depolamaktır."
            )
        ]
    })

    # ADIM 32
    slides.append({
        "slideNumber": 32,
        "title": "Anne Beslenmesini Bozan Riskli Gebelik Kriterleri",
        "subtitle": "Uç yaşlar (<18 veya >35), çok sayıda doğum (4+) ve düşük eğitim düzeyi",
        "badge": "Risk Faktörleri",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Halk sağlığı yaklaşımında gebe beslenmesini ve sağlığını doğrudan tehdit eden belirli demografik ve obstetrik 'riskli gebelik' "
            "özellikleri tanımlanmıştır. Bu özelliklerin başında anne yaşının uçlarda olması (<18 yaş adolesan gebelik veya >35 yaş ileri anne yaşı), "
            "kadının eğitim düzeyinin düşük olması ve doğum sayısının fazla olması (4 ve üzeri doğum - büyük multiparite) gelir.\n\n"
            "> [SINAV SPOTU] Açık uçlu kurul sınav sorusu: Annenin beslenmesini olumsuz etkileyen faktörler: Riskli gebelik özellikleri "
            "(<18 veya >35 yaş, düşük eğitim, 4+ doğum), sigara/alkol, kronik hastalıklar, emilim bozuklukları, ağır aktivite ve yetersiz DÖB'dür.\n\n"
            "Sık aralıklarla gerçekleşen çok sayıda doğum (maternal tükenmişlik sendromu), annenin demir ve kalsiyum depolarını tamamen eritir; "
            "18 yaş altındaki adölesan ise kendi kemik ve doku büyümesi ile fetüsün büyümesi arasında amansız bir besin rekabeti yaşar."
        ),
        "medicalTerms": [
            {"term": "Maternal Tükenmişlik Sendromu", "explanation": "İki yıldan kısa aralıklarla çok sayıda doğum yapan kadında mikrobesin ve kemik depolarının çökmesidir."},
            {"term": "Büyük Multiparite (Grand Multiparity)", "explanation": "Dört veya daha fazla canlı doğum yapmış olma durumudur; anemi ve atoni riskini katlar."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Riskli gebelik yaş sınırları: 18 yaş altı ve 35 yaş üstüdür.",
            "📌 [SINAV SPOTU] 4 ve üzeri doğum yapmış olmak (büyük multiparite) maternal depoları tüketerek malnütrisyon riskini artırır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "<18 ve >35 Yaş", "desc": "Uç yaşlar obstetrik ve besinsel komplikasyon riskini katlar.", "isKey": True},
                {"title": "4+ Doğum Yükü", "desc": "Maternal depolar yenilenmeden girilen gebelikler tükenme yaratır.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Anne beslenmesini olumsuz etkileyen obstetrik risk faktörleri arasında doğum sayısının 4 ve üzeri olması önemli yer tutar.",
                "4 ve üzeri",
                "Maternal depoları tüketen doğum sayısı eşiği"
            ),
            make_active_recall(
                "Anne beslenmesini olumsuz etkileyen obstetrik ve demografik riskli gebelik özellikleri nelerdir?",
                "Anne yaşının 18'in altında veya 35'in üstünde olması, düşük eğitim düzeyi ve doğum sayısının 4 ve üzeri (büyük multiparite) olmasıdır."
            )
        ]
    })

    # ADIM 33
    slides.append({
        "slideNumber": 33,
        "title": "Sosyoekonomik, Toksik ve Sistemik Etmenler",
        "subtitle": "Madde kullanımı, emilim bozuklukları, ağır fiziksel iş yükü ve DÖB yokluğu",
        "badge": "Sistemik Engeller",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Demografik risklerin ötesinde gebe beslenmesini derinden sarsan sistemik ve çevresel etkenler mevcuttur. Tütün mamulleri, "
            "alkol ve bağımlılık yapıcı toksik madde kullanımı; iştahı baskılamanın yanı sıra plasental kan akımını bozar ve teratojenik "
            "hasar üretir. Kronik sistemik hastalıklar (kronik böbrek yetmezliği, karaciğer hastalığı, inflamatuar bağırsak hastalıkları, çölyak) "
            "ise besin ögelerinin bağırsaktan emilimini ve hücresel biyoyararlanımını felce uğratır.\n\n"
            "> [SINAV SPOTU] Ağır fiziksel aktivite ve tarla/ağır ev işi yükü kadının harcadığı kaloriyi artırarak fetüse giden enerjiyi "
            "tüketir; yetersiz doğum öncesi bakım ise bu açığın tespit edilmesini imkansız kılar.\n\n"
            "Özellikle mevsimlik tarım işçisi kadınlarda aşırı kalori harcaması, yetersiz gıda alımı ve prenatal bakım yokluğu birleştiğinde "
            "ağır intrauterin gelişme geriliği kaçınılmaz hale gelir."
        ),
        "medicalTerms": [
            {"term": "Malabsorpsiyon (Emilim Bozukluğu)", "explanation": "Çölyak veya Crohn gibi hastalıklarda bağırsak villuslarının hasarıyla besinlerin kana geçememesidir."},
            {"term": "Enerji Negatif Dengesi", "explanation": "Harcanan enerjinin alınan gıdadan fazla olması sonucu vücudun kendi kas ve yağ dokusunu yıkmasıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Sigara, alkol ve toksik maddeler hem besin alımını bozar hem de plasental dolaşımı felç eder.",
            "📌 [SINAV SPOTU] Ağır fiziksel aktivite ve yetersiz DÖB maternal yetersiz beslenmenin en tehlikeli gizli tetikleyicileridir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Toksik Maddeler", "desc": "Nikotin ve alkol plasental transferi ve hücresel beslenmeyi yıkar.", "isKey": True},
                {"title": "Emilim Hasarı", "desc": "Kronik gastrointestinal patolojiler besin biyoyararlanımını sıfırlar.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Gebelikte anne beslenmesini bozan kronik hastalıklarda temel patoloji besin emiliminin bozulması ve biyoyararlanımın düşmesidir.",
                "besin emiliminin bozulması",
                "Gastrointestinal sindirim ve emilim kusuru"
            ),
            make_active_recall(
                "Ağır fiziksel aktivite ve kronik hastalıkların gebe beslenmesi üzerindeki ortak olumsuz biyolojik sonucu nedir?",
                "Artan metabolik harcama ve bozulan besin emilimi nedeniyle annenin negatif enerji dengesine girmesi ve fetal büyüme için gereken glukoz ve aminoasitlerin tükenmesidir."
            )
        ]
    })

    # ADIM 34
    slides.append({
        "slideNumber": 34,
        "title": "Yetersiz Beslenmenin Anne Üzerindeki Sonuçları",
        "subtitle": "Kendi dokularını eritme, ağır anemi, osteomalazi, toksemi ve mortalite",
        "badge": "Maternal Sonuçlar",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Gebelikte diyetle yeterli enerji ve besin ögeleri alınamadığında, fetüs biyolojik bir parazit gibi annenin depolarını "
            "sömürür. Gebe kadın kendi kas proteinlerini, karaciğer glikojenini ve kemik minerallerini harcamak (katabolizma) zorunda kalır. "
            "Bu durum annede ağır tükenmişlik, yetersiz ağırlık kazanımı ve enfeksiyonlara karşı bağışıklık çöküşü yaratır.\n\n"
            "> [SINAV SPOTU] Yetersiz beslenen annede gelişen majör patolojiler: Kendi dokularını harcama, demir ve folat eksikliği "
            "anemisi, kalsiyum kaybına bağlı OSTEOMALAZİ, toksemi (preeklampsi yatkınlığı), yaygın ödem ve anne ölümüdür.\n\n"
            "Özellikle D vitamini ve kalsiyum eksikliğinde paratiroid hormonunun aşırı uyarılması (sekonder hiperparatiroidizm) annenin "
            "uzun kemiklerini ve pelvisini yumuşatarak kalıcı iskelet deformitelerine (osteomalazi) yol açar."
        ),
        "medicalTerms": [
            {"term": "Osteomalazi", "explanation": "D vitamini ve kalsiyum eksikliğinde kemik osteoid dokusunun mineralize olamaması sonucu kemiklerin yumuşamasıdır."},
            {"term": "Maternal Katabolizma", "explanation": "Yetersiz beslenen gebenin fetüsü besleyebilmek için kendi kas ve yağ dokusunu yıkmasıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Maternal yetersiz beslenme: Doku harabiyeti, anemi, osteomalazi, toksemi ve anne ölümüne yol açar.",
            "📌 [SINAV SPOTU] Kalsiyum depolarının boşalması annede osteomalazi ve ileri yaşta şiddetli osteoporoza zemin hazırlar."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Doku Yıkımı", "desc": "Anne kendi kas ve kemik kitlesini fetüsün büyümesine feda eder.", "isKey": True},
                {"title": "Osteomalazi ve Anemi", "desc": "Kemik yumuşaması ve ağır eritrosit kaybı tabloya eşlik eder.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Gebelikte kalsiyum ve D vitamini yetersizliğinde annenin kemik mineralizasyonunun bozulmasıyla gelişen kemik yumuşaması tablosuna osteomalazi denir.",
                "osteomalazi",
                "Erişkinde kemik yumuşaması hastalığı"
            ),
            make_active_recall(
                "Yetersiz beslenen bir gebenin vücudunda ortaya çıkan 5 majör maternal klinik komplikasyon nedir?",
                "1. Kendi dokularını harcama (katabolizma), 2. Anemi (demir/folat eksikliği), 3. Osteomalazi (kemik yumuşaması), 4. Toksemi (preeklampsi yatkınlığı) ve ödem, 5. Anne ölümü."
            )
        ]
    })

    # ADIM 35
    slides.append({
        "slideNumber": 35,
        "title": "Yetersiz Beslenmenin Bebek Üzerindeki Sonuçları",
        "subtitle": "İntrauterin malnütrisyon, prematürite, DDA, spina bifida ve bebek ölümü",
        "badge": "Fetal Sonuçlar",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Gebelikte annenin yetersiz enerji ve besin ögesi alması, gelişmekte olan fetüs için yıkıcı sonuçlar doğurur. İntrauterin "
            "malnütrisyon ve fetal büyüme kısıtlılığı (IUGR), bebeğin düşük doğum ağırlıklı (<2500 g - DDA) veya prematüre (37 haftadan önce) "
            "dünyaya gelmesine yol açar; bu durum neonatal ölümlerin en büyük hazırlayıcısıdır.\n\n"
            "> [SINAV SPOTU] Gebelikte yetersiz enerji ve mikrobesin alımının fetal sonuçları: Prematürite, perinatal mortalite, "
            "SPİNA BİFİDA, hidrosefali, SSS malformasyonları ve kalıcı bedensel/zihinsel gelişim geriliğidir.\n\n"
            "Özellikle organogenez evresindeki folat, çinko ve iyot eksikliği; nöronal tüp kapanma kusurlarından kretenizme kadar "
            "geri dönüşsüz konjenital anomalilere yol açarak bebeğin entelektüel geleceğini karartır."
        ),
        "medicalTerms": [
            {"term": "Düşük Doğum Ağırlığı (DDA)", "explanation": "Gestasyonel yaştan bağımsız olarak bebeğin doğum tartısının 2500 gramın altında olmasıdır."},
            {"term": "İntrauterin Büyüme Kısıtlılığı (IUGR)", "explanation": "Fetüsün genetik büyüme potansiyeline plasental veya besinsel yetersizlik nedeniyle ulaşamamasıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Fetal yetersiz beslenme: Prematürite, DDA, perinatal ölüm, spina bifida ve hidrosefaliye yol açar.",
            "📌 [SINAV SPOTU] İntrauterin dönemde yaşanan besin açığı kalıcı bedensel ve mental retardasyon üretir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "DDA ve Prematürite", "desc": "Doğum ağırlığının 2500 g altına düşmesi bebek mortalitesini katlar.", "isKey": True},
                {"title": "Nöral Tüp Kusurları", "desc": "Spina bifida ve hidrosefali mikrobesin açığının doğrudan sonucudur.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Gebelikte folik asit ve enerji yetersizliğinde bebekte omuriliğin açık kalmasıyla seyreden nöral tüp defektine spina bifida denir.",
                "spina bifida",
                "Ayrık omurga anomalisi"
            ),
            make_active_recall(
                "Maternal beslenme yetersizliğinin bebek üzerinde yarattığı 4 majör fetal-neonatal sonuç nedir?",
                "1. Düşük doğum ağırlığı (<2500 g) ve prematürite, 2. Spina bifida ve hidrosefali gibi SSS anomalileri, 3. Bedensel ve zihinsel gelişim geriliği, 4. Perinatal bebek ölümü."
            )
        ]
    })

    # ADIM 36
    slides.append({
        "slideNumber": 36,
        "title": "Aşırı Beslenmenin Maternal Riskleri: Gestasyonel Diyabet ve Toksemi",
        "subtitle": "İnsülin direncinin dekompanse olması, hipertansiyon ve güç doğum",
        "badge": "Aşırı Beslenme",
        "badgeColor": "amber",
        "synthesisNarrative": (
            "Gebelikte 'iki canlı' yanılgısıyla aşırı enerji ve basit karbonhidrat tüketimi, en az yetersiz beslenme kadar tehlikeli "
            "obstetrik tablolara yol açar. Gebeliğin ikinci yarısında plasental laktojen (hPL) ve progesteron nedeniyle zaten fizyolojik "
            "bir insülin direnci mevcuttur. Anne aşırı beslendiğinde pankreas beta hücreleri artan ihtiyacı karşılayamaz ve Gestasyonel "
            "Diabetes Mellitus (GDM) patlak verir.\n\n"
            "> [SINAV SPOTU] Aşırı beslenme ve fazla enerji alımının maternal sonuçları: Enerji dengesizliği, GESTASYONEL DİYABET, "
            "hipertansiyon, preeklampsi, güç doğum, sezaryen doğum oranı artışı ve doğum sonrası kalıcı kilo (maternal obezite) kalmasıdır.\n\n"
            "Aşırı adipoz doku kaynaklı proinflamatuar sitokinler endotel hasarını tetikleyerek preeklampsi riskini katbekat yükseltir; "
            "aynı zamanda yumuşak doğum kanalında aşırı yağ birikmesi travayı mekanik olarak güçleştirir."
        ),
        "medicalTerms": [
            {"term": "Gestasyonel Diyabet (GDM)", "explanation": "İlk kez gebelik sırasında ortaya çıkan veya tanınan herhangi bir derecedeki glukoz intoleransıdır."},
            {"term": "Doğum Sonrası Kalıcı Kilo", "explanation": "Gebelikte aşırı alınan yağ kütlesinin lohusalıkta verilemeyerek kronik obeziteye dönüşmesidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Aşırı beslenme maternal gestasyonel diyabet, preeklampsi ve sezaryen riskini dramatik artırır.",
            "📌 [SINAV SPOTU] Gebelikte aşırı kilo alımı lohusalık sonrasında annede kalıcı metabolik sendrom bırakır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "GDM Patlaması", "desc": "Aşırı kalori fizyolojik insülin direncini klinik diyabete dönüştürür.", "isKey": True},
                {"title": "Güç Doğum ve Sezaryen", "desc": "Maternal pelvik yağ dokusu ve fetal irilik cerrahi doğumu zorunlu kılar.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Gebelikte aşırı enerji ve karbonhidrat alımı plasental hormonların tetiklediği insülin direnci zemininde gestasyonel diyabet tablosuna yol açar.",
                "gestasyonel diyabet",
                "Gebelikte ortaya çıkan şeker hastalığı"
            ),
            make_active_recall(
                "Aşırı beslenen ve fazla enerji alan bir gebede gelişme riski en yüksek olan 4 temel maternal komplikasyon nedir?",
                "1. Gestasyonel diyabet, 2. Preeklampsi ve hipertansiyon, 3. Güç doğum ve zorunlu sezaryen, 4. Doğum sonrası kalıcı kilo ve obezite."
            )
        ]
    })

    # ADIM 37
    slides.append({
        "slideNumber": 37,
        "title": "Aşırı Beslenmenin Fetal Riskleri: Makrozomi ve Doğum Hasarı",
        "subtitle": "Maternal hipergliseminin fetal hiperinsülinizm ve organ büyümesi yaratması",
        "badge": "Fetal Makrozomi",
        "badgeColor": "amber",
        "synthesisNarrative": (
            "Annenin aşırı beslenmesi ve kan glukozunun kontrolsüz yükselmesi Pedersen hipotezi ile açıklanan fetal komplikasyonları doğurur. "
            "Maternal glukoz plasentadan kolaylaştırılmış difüzyonla fetüse geçer; ancak maternal insülin plasentayı geçemez. Fetüsün "
            "kendi pankreası bu aşırı glukoz yüküne hiperinsülinizm ile yanıt verir. İnsülin fetüste en güçlü büyüme hormonudur.\n\n"
            "> [SINAV SPOTU] Aşırı beslenmenin fetal-neonatal sonuçları: MAKROZOMİ (>4000-4500 g iri bebek), omuz distosisi, "
            "doğum travmaları (brakial pleksus felci), ölü doğum, neonatal hipoglisemi ve çocukluk çağı obezitesidir.\n\n"
            "Doğum kanalına takılan geniş omuzlar klavikula kırığına ve Erb-Duchenne felcine yol açarken; kord klemplendiğinde maternal "
            "glukoz aniden kesilir ama bebeğin hiperinsülinizmi sürdüğü için ölümcül neonatal hipoglisemi gelişir."
        ),
        "medicalTerms": [
            {"term": "Fetal Makrozomi", "explanation": "Bebeğin tahmini veya doğum tartısının 4000 veya 4500 gramın üzerinde olması durumudur."},
            {"term": "Omuz Distosisi", "explanation": "Fetal baş doğduktan sonra irileşen ön omzun maternal simfizis pubise takılarak takılı kalması acilidir."},
            {"term": "Neonatal Hipoglisemi", "explanation": "Doğumda hiperinsülinik bebeğin kan şekerinin aniden 40 mg/dl altına düşmesidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Aşırı beslenme fetal makrozomi, doğum travması, ölü doğum ve neonatal hipoglisemiye yol açar.",
            "📌 [SINAV SPOTU] İntrauterin hiperinsülinizm yenidoğanda doğum sonrası saatlerde ağır hipoglisemi nöbeti yaratır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Makrozomi Tuzağı", "desc": "Fetal hiperinsülinizm omuz ve gövde yağlanmasını aşırı artırır.", "isKey": True},
                {"title": "Omuz Distosisi", "desc": "Doğum kanalında takılma brakial pleksus felci ve asfiksi yapar.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Aşırı beslenen annelerin bebeklerinde fetal hiperinsülinizme bağlı olarak doğum tartısının 4000 gram üstüne çıkmasına makrozomi adı verilir.",
                "makrozomi",
                "İri bebek tablosu"
            ),
            make_active_recall(
                "Diyabetik veya aşırı beslenen annenin bebeğinde kord kesildikten hemen sonra neden şiddetli neonatal hipoglisemi gelişir?",
                "Anne karnında sürekli yüksek glukoza maruz kalan fetüsün pankreası aşırı insülin üretir. Kordon kesilince anneden gelen glukoz aniden sıfırlanır ancak kandaki yüksek fetal insülin mevcut şekeri hızla tüketerek hipoglisemi yapar."
            )
        ]
    })

    # ADIM 38
    slides.append({
        "slideNumber": 38,
        "title": "Maternal-Fetal Beslenme Dengesi Matrisi",
        "subtitle": "Yetersiz ve aşırı beslenmenin karşılaştırmalı patolojik tablosu",
        "badge": "Sentez Matrisi",
        "badgeColor": "teal",
        "synthesisNarrative": (
            "Gebelikte beslenmenin spektrumunu netleştirmek adına yetersiz beslenme ile aşırı beslenmenin anne ve bebek üzerindeki "
            "yansımalarını bir matris halinde değerlendirmek klinik ayırıcı tanı ve hasta yönetimi için esastır. Her iki durum da "
            "perinatal mortaliteyi ve anne morbiditesini artıran iki zıt kutup olmakla birlikte, optimal gebelik ancak 'öglisemik ve "
            "ömetabolik' bir dar koridorda sürdürülebilir.\n\n"
            "> [SINAV SPOTU] Yetersiz beslenme Düşük Doğum Ağırlığı (DDA) ve IUGR yaparken; aşırı beslenme Makrozomi ve Gestasyonel "
            "Diyabet yapar. Her iki uç nokta da prematürite ve perinatal ölüm riskini artırır!\n\n"
            "Bu dengeyi sağlamanın yegane yolu; gebenin gebelik öncesi beden kitle indeksine (BKİ) göre hedeflenen ağırlık kazanımını "
            "düzenli kilo takipleriyle izlemek ve trimesterlere özgü enerji eklemelerini harfiyen uygulamaktır."
        ),
        "medicalTerms": [
            {"term": "Perinatal Mortalite", "explanation": "22. gebelik haftasından doğum sonrası ilk 7 güne kadar gerçekleşen fetal ve neonatal ölümlerdir."},
            {"term": "Metabolik Koridor", "explanation": "Gebelikte ne ketozise ne de hiperglisemiye girmeden tutulan ideal glukoz aralığıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] İki uç tablo: Yetersiz beslenme = DDA + Osteomalazi; Aşırı beslenme = Makrozomi + GDM + Preeklampsi.",
            "📌 [SINAV SPOTU] Hem yetersiz hem aşırı kalori alımı ortak paydada prematüre doğum ve perinatal mortaliteyi artırır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Zıt Kutuplar", "desc": "Bir uçta malnütrisyon ve organ hipoplazisi, diğer uçta makrozomi ve distosi.", "isKey": True},
                {"title": "Ortak Tehdit", "desc": "Her iki dengesizlik de erken doğum ve bebek kaybı ile sonuçlanabilir.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "Yetersiz Beslenme vs Aşırı Beslenmenin Maternal-Fetal Yansımaları",
                "Yetersiz Beslenme Tablosu",
                "Annede doku harabiyeti, anemi ve osteomalazi; bebekte intrauterin büyüme geriliği, düşük doğum ağırlığı (<2500 g), spina bifida ve mental gerilik gelişir.",
                "Aşırı Beslenme Tablosu",
                "Annede gestasyonel diyabet, hipertansiyon, preeklampsi ve sezaryen zorunluluğu; bebekte makrozomi (>4000 g), omuz distosisi ve neonatal hipoglisemi gelişir."
            ),
            make_active_recall(
                "Hem yetersiz beslenmede hem de aşırı beslenmede ortak olarak artış gösteren iki obstetrik komplikasyon nedir?",
                "Prematüre doğum (preterm eylem) ve perinatal bebek ölümüdür (ölü doğum veya erken neonatal kayıp)."
            )
        ]
    })

    # ADIM 39 [CHECKPOINT 4]
    slides.append({
        "slideNumber": 39,
        "title": "[TEKRAR SAYFASI - CHECKPOINT 4] Yetersiz ve Aşırı Beslenme İstasyonu",
        "subtitle": "Maternal risk faktörleri, IUGR, makrozomi ve GDM bileşenlerinin konsolidasyonu",
        "badge": "Checkpoint",
        "badgeColor": "teal",
        "isCheckpoint": True,
        "checkpointNumber": 4,
        "synthesisNarrative": (
            "Bu istasyon; gebelikte beslenmenin 4 amacını, 'iki canlı' efsanesinin çürütülmesini, riskli gebelik parametrelerini "
            "(<18 veya >35 yaş, 4+ doğum, kronik hastalık, ağır iş), yetersiz beslenmenin annede yarattığı doku kaybı, osteomalazi ve "
            "anemi ile bebekte yaptığı IUGR, DDA (<2500 g) ve spina bifidayı; aşırı beslenmenin annede yaptığı GDM, preeklampsi ve kalıcı "
            "kilo ile bebekte yaptığı makrozomi (>4000 g), omuz distosisi ve neonatal hipoglisemiyi sentezlemektedir.\n\n"
            "> [YÜKSEK VERİM] Riskli gebelik = <18 veya >35 yaş, 4+ doğum; Yetersiz beslenme = Annede osteomalazi/anemi, bebekte "
            "DDA/spina bifida; Aşırı beslenme = Annede GDM/HT/sezaryen, bebekte makrozomi/omuz distosisi/hipoglisemi."
        ),
        "medicalTerms": [
            {"term": "Gestasyonel Spektrum", "explanation": "Malnütrisyondan makrozomiye uzanan fetal kilo ve metabolizma dağılımıdır."},
            {"term": "DDA vs Makrozomi", "explanation": "Doğum ağırlığının <2500 g (DDA) veya >4000 g (makrozomi) olması sınırlarıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Anne beslenmesini bozan riskler: Yaş (<18 veya >35), çok doğum (4+), madde kullanımı, emilim bozukluğu.",
            "📌 [SINAV SPOTU] Yetersiz beslenme: Doku harcanması, anemi, osteomalazi; bebekte DDA, spina bifida, gelişim geriliği.",
            "📌 [SINAV SPOTU] Aşırı beslenme: GDM, preeklampsi, sezaryen; bebekte makrozomi, omuz distosisi, neonatal hipoglisemi."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Risk Triadı", "desc": "Uç yaşlar, yüksek doğum sayısı ve sosyoekonomik yoksunluk.", "isKey": True},
                {"title": "Fetal Çıktılar", "desc": "Kıtlıkta DDA ve NTD; bollukta makrozomi ve omuz distosisi.", "isKey": True},
                {"title": "Maternal Çıktılar", "desc": "Kıtlıkta osteomalazi ve anemi; fazlalıkta GDM ve toksemi.", "isKey": True}
            ]
        },
        "flashcards": [
            make_flashcard(
                "fc-k1-06-10",
                "Gebelikte anne beslenmesini olumsuz etkileyen demografik ve obstetrik risk faktörleri nelerdir?",
                "Anne yaşının 18 altı veya 35 üstü olması, düşük eğitim düzeyi ve doğum sayısının 4 ve üzeri olmasıdır.",
                "Riskli gebelik kriterleri"
            ),
            make_flashcard(
                "fc-k1-06-11",
                "Yetersiz beslenen bir annede ve bebeğinde görülen en karakteristik ikişer klinik patoloji nedir?",
                "Annede: Osteomalazi ve ağır anemi.\nBebekte: Düşük doğum ağırlığı (<2500 g) ve spina bifida/nöral tüp defekti.",
                "Yetersiz beslenme sonuçları"
            ),
            make_flashcard(
                "fc-k1-06-12",
                "Aşırı beslenen bir annede ve bebeğinde ortaya çıkan en karakteristik ikişer patoloji nedir?",
                "Annede: Gestasyonel diyabet (GDM) ve preeklampsi.\nBebekte: Fetal makrozomi (>4000 g) ve omuz distosisi / neonatal hipoglisemi.",
                "Aşırı beslenme komplikasyonları"
            )
        ],
        "interactiveElements": [
            make_table(
                ["Beslenme Durumu", "Anne Üzerindeki Temel Sonuç", "Bebek Üzerindeki Temel Sonuç"],
                [
                    [("Yetersiz Beslenme", False, ""), ("Doku yıkımı, anemi ve osteomalazi", True, "Annede kemik yumuşaması ve kan kaybı tablosu"), ("İntrauterin büyüme kısıtlılığı ve düşük doğum ağırlığı", False, "")],
                    [("Aşırı Beslenme", False, ""), ("Gestasyonel diyabet, hipertansiyon ve zorunlu sezaryen", False, ""), ("Makrozomi, omuz distosisi ve neonatal hipoglisemi", True, "İri bebek ve doğum kanalı travması")]
                ]
            )
        ]
    })

    # ADIM 40
    slides.append({
        "slideNumber": 40,
        "title": "Gestasyonel Diyabet (GDM) Taraması ve Yönetim İlkeleri",
        "subtitle": "24-28. haftalarda oral glukoz tolerans testi (OGTT) ve diyet tedavisi",
        "badge": "GDM Taraması",
        "badgeColor": "amber",
        "synthesisNarrative": (
            "Gebelikte aşırı beslenmenin ve genetik yatkınlığın en sık klinik sonucu olan Gestasyonel Diabetes Mellitus (GDM), "
            "genellikle gebeliğin 24. ve 28. haftaları arasında plasental hormonların (hPL, kortizol, progesteron) pik yapmasıyla "
            "belirginleşir. Bu nedenle tüm gebelere 24-28. haftalarda standart Oral Glukoz Tolerans Testi (OGTT: 50 g tarama veya "
            "75 g tek aşamalı tanı testi) uygulanması ulusal ve uluslararası kılavuzlarca önerilir.\n\n"
            "> [SINAV SPOTU] Gestasyonel diyabet tanısı alan gebede İLK TEDAVİ ADIMI İLAÇ DEĞİL; tıbbi beslenme tedavisi (diyet) "
            "ve uygun egzersizdir. Hedef kan şekeri açlıkta <95 mg/dl, tokluk 1. saatte <140 mg/dl tutulmalıdır.\n\n"
            "Diyetle glukoz hedeflerine ulaşılamayan olgularda plasentayı geçmeyen insülin tedavisine başlanır. Erken tanı ve diyet, "
            "fetal makrozomiyi ve yenidoğan yoğun bakım yatışlarını %50'den fazla azaltır."
        ),
        "medicalTerms": [
            {"term": "Oral Glukoz Tolerans Testi (OGTT)", "explanation": "Gebeliğin 24-28. haftalarında glukoz içirilerek diyabet taraması ve tanısı koyduran standart testtir."},
            {"term": "Tıbbi Beslenme Tedavisi (TBT)", "explanation": "Diyabetli gebede glisemik kontrolü sağlayan karbonhidrat kısıtlı ve lif zengin bireysel diyet planıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] GDM tarama ve tanı haftası: 24-28. gebelik haftalarıdır.",
            "📌 [SINAV SPOTU] GDM yönetiminde ilk basamak daima tıbbi beslenme tedavisi (diyet) ve hafif egzersizdir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "24-28. Hafta", "desc": "Plasental hormonların insülini en çok bloke ettiği tanı aralığıdır.", "isKey": True},
                {"title": "Önce Diyet", "desc": "Tıbbi beslenme tedavisi başarısız olursa insüline geçilir.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Gestasyonel diyabet taraması plasental hormonların pik yaptığı 24-28. gebelik haftaları arasında oral glukoz tolerans testiyle yapılır.",
                "24-28. gebelik haftaları",
                "Diyabet taramasının yapıldığı rutin gebelik haftası aralığı"
            ),
            make_active_recall(
                "Gestasyonel diabetes mellitus (GDM) taraması rutin olarak hangi gebelik haftalarında yapılır ve tanıda ilk tedavi adımı nedir?",
                "24-28. gebelik haftalarında yapılır. Tanı konduğunda ilk tedavi adımı ilaç veya insülin değil; tıbbi beslenme tedavisi (diyet) ve hafif egzersizdir."
            )
        ]
    })

    return slides
