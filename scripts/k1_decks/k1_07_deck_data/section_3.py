"""
Bölüm 3: Kolesterol ve Kolesteril Ester Birikimleri: Ateroskleroz, Ksantomlar ve Kolesterolozis
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
        "title": "Kolesterolün Hücresel Rolü ve Sıkı Homeostaz Mekanizmaları",
        "subtitle": "Membran akışkanlığı, steroid sentezi ve hücre içi kolesterol denetimi",
        "badge": "Kolesterol Fizyolojisi",
        "badgeColor": "amber",
        "synthesisNarrative": (
            "Kolesterol, ökaryotik hücre membranlarının temel yapı taşı olup zar akışkanlığının, membran mikro-alanlarının "
            "(lipid salları) ve steroid hormon sentezinin vazgeçilmez molekülüdür. Hücreler kolesterolü iki yolla elde eder: "
            "asetil-KoA'dan de novo sentez (HMG-KoA redüktaz) veya kandan LDL reseptörleri aracılığıyla endositoz.\n\n"
            "> [TEMEL İLKE] Kolesterol hücre için hayati olmakla birlikte yıkılamaz; fazla kolesterol esterleştirilerek "
            "(ACAT enzimiyle kolesteril ester) saklanır veya HDL aracılığıyla karaciğere geri taşınır.\n\n"
            "Hücre içi serbest kolesterol miktarı SREBP ve LXR transkripsiyon faktörleri tarafından son derece sıkı denetlenir. "
            "Bu kontrol aşıldığında toksik kolesterol birikimi başlar."
        ),
        "medicalTerms": [
            {"term": "Kolesterol", "explanation": "Hücre membran yapısına katılan ve steroidlerin öncülü olan 27 karbonlu steroldür."},
            {"term": "Kolesteril Ester", "explanation": "Kolesterolün yağ asidiyle esterleşmiş, hücre içi damlacıklarda depolanan formudur."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Hücreler kolesterol halkasını parçalayamaz; ya esterleştirir ya da HDL ile atar.",
            "📌 [SINAV SPOTU] Hücre içine kolesterol girişi primer olarak LDL reseptörleri üzerinden yürütülür."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Membran Desteği", "desc": "Plazma membran bütünlüğü ve geçirgenlik bariyeri.", "isKey": True},
                {"title": "Yıkılamaz Sterol", "desc": "Katabolize edilemez; safra asitlerine dönüşüm karaciğere aittir.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Hücre içinde fazla kolesterol, ACAT enzimi aracılığıyla kolesteril ester formuna dönüştürülerek depolanır.",
                "kolesteril ester",
                "Kolesterolün depolanan nötral ester formu"
            ),
            make_active_recall(
                "Hücrelerin kolesterol molekülünü parçalamak konusundaki en temel metabolik kısıtlılığı nedir?",
                "Memeli hücreleri kolesterolün dört halkalı sterol çekirdeğini parçalayamaz; fazlalığı ya dışarı atmak ya da esterleştirmek zorundadır."
            )
        ]
    })

    # ADIM 22
    slides.append({
        "slideNumber": 22,
        "title": "Aşırı Kolesterol Yükü ve Makrofaj / Düz Kas Hücresi Yanıtı",
        "subtitle": "Okside LDL, çöpçü (scavenger) reseptörler ve geri bildirimsiz alım",
        "badge": "Aşırı Yük Yanıtı",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Dolaşımda LDL düzeyi yükseldiğinde veya intima tabakasında endotel hasarı geliştiğinde, LDL molekülleri "
            "damar duvarına sızar ve reaktif oksijen türleri tarafından okside edilir (oxLDL). Normal LDL reseptörleri "
            "kolesterol arttığında negatif geri bildirimle baskılanırken, makrofajların çöpçü reseptörleri (SR-A, CD36) "
            "oxLDL'yi kontrolsüz ve sınırsız şekilde yutmaya devam eder.\n\n"
            "> [SINAV SPOTU] Çöpçü reseptörlerde aşağı regülasyon (down-regulation) yoktur; bu durum makrofajların "
            "kolesteril esterle patlayana kadar dolmasına neden olur.\n\n"
            "Benzer şekilde tunika mediadan intimaya göç eden damar düz kas hücreleri de bu lipidleri alarak köpüklü "
            "bir görünüme bürünür."
        ),
        "medicalTerms": [
            {"term": "Okside LDL (oxLDL)", "explanation": "Damar duvarında serbest radikallerle modifiye olmuş, immünojenik ve toksik LDL'dir."},
            {"term": "Çöpçü (Scavenger) Reseptör", "explanation": "Makrofajlarda bulunan ve oxLDL'yi geri bildirimsiz yutan reseptörlerdir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Makrofaj çöpçü reseptörleri negatif geri bildirim göstermez; sınırsız lipid alırlar.",
            "📌 [SINAV SPOTU] Damar duvarında lipid toplayan hücreler hem makrofajlar hem de vasküler düz kas hücreleridir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Geri Bildirimsiz Yutma", "desc": "Çöpçü reseptörler hücre içi kolesterol artsa da kapanmaz.", "isKey": True},
                {"title": "oxLDL Sitotoksisitesi", "desc": "İnflamatuvar sitokin salınımını ve hücre ölümünü tetikler.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_micro_quiz(
                "Makrofajların ateroskleroz sürecinde aşırı miktarda kolesterol depolayarak köpük hücreye dönüşmesinde rol oynayan en temel reseptör mekanizması hangisidir?",
                {
                    "A": "Klasik LDL reseptörlerinin aşırı uyarılması",
                    "B": "Çöpçü (scavenger) reseptörlerin oxLDL alımında negatif geri bildirim göstermemesi",
                    "C": "VLDL reseptörlerinin endoplazmik retikuluma kaçması",
                    "D": "HDL reseptörü SR-BI'nın apoptozu engellemesi",
                    "E": "İnsülin reseptörlerinin tirozin kinaz mutasyonu"
                },
                "B",
                {
                    "A": "Klasik LDL reseptörü hücre içi kolesterol artınca kapanır (down-regüle olur).",
                    "B": "Doğru! Çöpçü reseptörler (CD36, SR-A) geri bildirimsizdir; makrofaj doymaksızın oxLDL yutar.",
                    "C": "VLDL reseptörü değil oxLDL çöpçü reseptörleri primer sorumludur.",
                    "D": "SR-BI kolesterol çıkışını sağlar, aşırı birikim nedeni değildir.",
                    "E": "İnsülin reseptör mutasyonu köpük hücreye dönüşümün primer sebebi değildir."
                }
            ),
            make_cloze(
                "Makrofajların oxLDL alımından sorumlu olan çöpçü reseptörler kolesterol birikimiyle down-regüle olmaz.",
                "çöpçü",
                "Negatif geri bildirimi olmayan lipid yutucu reseptör tipi"
            )
        ]
    })

    # ADIM 23
    slides.append({
        "slideNumber": 23,
        "title": "Köpük Hücre (Foam Cell) Biyolojisi ve Morfolojik Özellikleri",
        "subtitle": "Kolesteril ester dolu vakuollerin ışık mikroskobundaki karakteristik görünümü",
        "badge": "Köpük Hücre",
        "badgeColor": "blue",
        "synthesisNarrative": (
            "Köpük hücre (foam cell), sitoplazması yüzlerce minik kolesterol ve kolesteril ester damlacığıyla dolmuş "
            "makrofaj veya düz kas hücresidir. Rutin hematoksilen-eozin (H&E) preparatlarının hazırlanması sırasında "
            "kullanılan ksilol ve alkol gibi organik çözücüler lipidleri erittiği için, bu damlacıkların yerinde boşluklar "
            "kalır. Bu durum sitoplazmaya karakteristik sabun köpüğü veya dantel benzeri açık renkli, vakuollü bir görünüm kazandırır.\n\n"
            "> [YÜKSEK VERİM] Köpük hücreler lipidleri yalnızca depolamaz; sitokinler (IL-1, TNF), kemokinler ve reaktif "
            "oksijen türleri salgılayarak lokal yangıyı sürekli alevlendirir.\n\n"
            "Zamanla aşırı lipid yükü köpük hücrelerde apoptoz ve nekrozu tetikleyerek nekrotik çekirdeği besler."
        ),
        "medicalTerms": [
            {"term": "Köpük Hücre (Foam Cell)", "explanation": "Sitoplazması kolesteril ester damlacıklarıyla dolu, köpüksü görünümlü makrofaj veya düz kas hücresidir."},
            {"term": "Lipid Erimesi", "explanation": "Rutin histolojik fiksasyonda alkol/ksilolün lipidleri eritip boş vakuol bırakmasıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Rutin H&E kesitlerinde köpük hücrelerin sitoplazması açık renkli ve vakuollü görünür.",
            "📌 [SINAV SPOTU] Köpük hücrelerin kökeni doku makrofajları ve intimaya göç eden düz kas hücreleridir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Morfolojik İmza", "desc": "İnce vakuollü, açık renkli köpüksü sitoplazma.", "isKey": True},
                {"title": "İnflamatuvar Rol", "desc": "Sitokin ve kemokin üreterek lezyonun büyümesini sürdürür.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "İstirahat Makrofajı vs Köpük Hücre",
                "İstirahat Makrofajı",
                "Dar eozinofilik sitoplazma, minimal lipid içeriği ve fagositoza hazır bazal immün hücre profili.",
                "Köpük Hücre (Foam Cell)",
                "Kolesteril ester damlacıklarıyla şişmiş geniş, açık renkli vakuollü sitoplazma ve yüksek sitokin salgısı."
            ),
            make_active_recall(
                "Köpük hücrelerin mikroskop altında köpüksü görünmesinin histolojik hazırlıkla ilişkisi nedir?",
                "Rutin doku takibinde alkol ve ksilol lipid damlacıklarını erittiği için geride optik olarak boş vakuoller kalır ve köpüksü görünüm doğar."
            )
        ]
    })

    # ADIM 24
    slides.append({
        "slideNumber": 24,
        "title": "Ateroskleroz Patogenezinde Kolesterol: İntimal Plak ve Kristaller",
        "subtitle": "Yağlı çizgilenmeden fibröz ateromatöz plağa uzanan lezyon evrimi",
        "badge": "Ateroskleroz",
        "badgeColor": "teal",
        "synthesisNarrative": (
            "Ateroskleroz, büyük ve elastik arterler (aort, karotis) ile orta çaplı muskuler arterlerin (koroner, "
            "popliteal) intima tabakasında lipid birikimiyle başlayan kronik inflamatuvar ve fibroproliferatif bir hastalıktır. "
            "Lezyonun en erken evresi çocukluk çağında dahi görülebilen 'yağlı çizgilenme' (fatty streak) olup intimada "
            "köpük hücre kümelerinden ibarettir.\n\n"
            "> [SINAV SPOTU] İlerleyen evrede köpük hücrelerin nekroza uğramasıyla ekstraselüler alana kolesterol kristalleri "
            "dökülür; bu kristaller histolojide iğsi 'kolesterol yarıkları' (cholesterol clefts) olarak izlenir.\n\n"
            "Düz kas hücrelerinin ürettiği kollajenöz fibröz şapka nekrotik lipid çekirdeğin üzerini örterek ateromatöz plağı tamamlar."
        ),
        "medicalTerms": [
            {"term": "Ateromatöz Plak", "explanation": "Nekrotik lipid çekirdek ve üzerindeki fibröz başlıktan oluşan aterosklerotik lezyondur."},
            {"term": "Kolesterol Yarığı", "explanation": "Histolojik takipte eriyen ekstraselüler kolesterol kristallerinin bıraktığı iğsi boşluklardır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Aterosklerozun en erken mikroskobik lezyonu intimadaki köpük hücrelerden oluşan yağlı çizgilenmedir.",
            "📌 [SINAV SPOTU] Plak merkezinde eriyen kolesterol kristalleri histolojide iğsi yarıklar olarak görülür."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Yağlı Çizgilenme", "desc": "İntimada toplanmış saf köpük hücre yığınları, lümeni daraltmaz.", "isKey": True},
                {"title": "Aterom Plağı", "desc": "Nekrotik lipid havuzu, kolesterol kristalleri ve fibröz kapsül.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_causal_chain(
                "Aterosklerotik Plağın Oluşum Zinciri",
                [
                    "1. Endotel Hasarı: Hemodinamik stres ve hiperlipidemi endotel geçirgenliğini artırır.",
                    "2. oxLDL ve Fagositoz: İntimaya geçen LDL oksitlenir ve makrofajlarca çöpçü reseptörlerle yutulur.",
                    "3. Köpük Hücre Birikimi: İntimada köpük hücreler toplanarak yağlı çizgilenmeyi (fatty streak) yapar.",
                    "4. Nekrotik Çekirdek: Köpük hücreler apoptoz/nekroza uğrar; ekstraselüler kolesterol kristalleri çöker.",
                    "5. Fibröz Şapka: Düz kas hücreleri kollajen sentezleyerek lipid gölünün üzerini fibröz örtüyle kapatır."
                ]
            ),
            make_cloze(
                "Aterom plağının nekrotik merkezinde kolesterol kristallerinin erimesiyle oluşan iğsi boşluklara kolesterol yarıkları denir.",
                "kolesterol yarıkları",
                "Histolojik kesitlerde kristallerin bıraktığı iğsi boşluklar"
            )
        ]
    })

    # ADIM 25
    slides.append({
        "slideNumber": 25,
        "title": "Ateromatöz Plakta Hücre İçi ve Hücre Dışı Kolesterol Dağılımı",
        "subtitle": "Stabil plaktan frajil ve kalsifiye plağa geçişin yapısal dinamikleri",
        "badge": "Plak Dinamiği",
        "badgeColor": "stone",
        "synthesisNarrative": (
            "Ateromatöz plakta lipidler iki kompartımanda dağılır: hücre içi (köpük hücrelerin sitoplazmasında) ve "
            "hücre dışı (nekrotik çekirdekte serbest kristalize kolesterol ve kolesteril esterler halinde). Stabil "
            "plaklarda kalın bir fibröz başlık ve minimal nekrotik çekirdek bulunurken; kararsız (vulnerabl) plaklarda "
            "ince bir fibröz şapka, devasa nekrotik lipid çekirdeği ve yoğun köpük hücre inflamasyonu mevcuttur.\n\n"
            "> [KRİTİK UYARI] Ekstraselüler kolesterol kristalleri NLRP3 inflamazomunu doğrudan aktive ederek IL-1β "
            "salınımını kamçılar ve plağın rüptür (yırtılma) riskini katlar.\n\n"
            "Ayrıca nekrotik hücre artıklarının bulunduğu alanda distrofik kalsifikasyon gelişerek damar duvarını sertleştirir."
        ),
        "medicalTerms": [
            {"term": "Vulnerabl Plak", "explanation": "İnce fibröz başlıklı, geniş lipid göletli ve yırtılmaya eğilimli frajil aterom plağıdır."},
            {"term": "NLRP3 İnflamazomu", "explanation": "Kolesterol kristallerini yabancı tehlike sinyali algılayıp IL-1 üreten sitozolik komplekstir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Serbest kolesterol kristalleri inflamazomu aktive ederek plağı destabilize eder.",
            "📌 [SINAV SPOTU] Plak yırtılması akut tromboz ve miyokard enfarktüsünün primer tetikleyicisidir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Hücre İçi Havuz", "desc": "Köpük makrofajlar ve düz kas hücrelerinde vakuoler esterler.", "isKey": True},
                {"title": "Hücre Dışı Havuz", "desc": "Nekrotik merkezde kristalize yarıklar ve kalsiyum tuzları.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Plak Özelliği", "Stabil Aterom Plağı", "Vulnerabl (Kararsız) Plak"],
                [
                    [("Fibröz Başlık", False, ""), ("Kalın, yoğun kollajen lifler", False, ""), ("İnce, frajil, kollajenden fakir", True, "Yırtılmaya aşırı duyarlı örtü")],
                    [("Nekrotik Lipid Çekirdeği", False, ""), ("Küçük, sınırlandırılmış", False, ""), ("Geniş, masif kolesterol göleti", True, "Hacmin yüzde 40'ından fazlası")],
                    [("İnflamatuvar Köpük Hücre", False, ""), ("Az sayıda, sessiz", False, ""), ("Çok yoğun makrofaj infiltrasyonu", True, "Matriks metalloproteinaz salgılayan hücreler")]
                ]
            ),
            make_cloze(
                "Ateromatöz plakta serbest kolesterol kristalleri makrofaj sitozolündeki inflamazom kompleksini uyararak inflamasyonu körükler.",
                "inflamazom",
                "Kristalleri algılayıp interlökin üreten protein kompleksi"
            )
        ]
    })

    # ADIM 26
    slides.append({
        "slideNumber": 26,
        "title": "Ksantomlar (Ksantelazma, Tuberoerüptif, Tendon Ksantomları)",
        "subtitle": "Deri ve tendon konnektif dokusunda kolesterol yüklü makrofaj tümörleri",
        "badge": "Ksantomlar",
        "badgeColor": "indigo",
        "synthesisNarrative": (
            "Ksantomlar, derinin subepitelyal bağ dokusunda veya tendonlarda kolesterol ve kolesteril esterle tıka basa "
            "dolmuş histiositlerin (makrofajların) fokal olarak kümelenmesiyle oluşan sarımsı nodül, plak ve kitlelerdir. "
            "Ksantom neoplastik bir tümör değil, lokalize bir hücre içi kolesterol depolanma lezyonudur.\n\n"
            "> [YÜKSEK VERİM] Göz kapaklarının medial kanto-orbital bölgesinde yerleşen düz sarımsı plaklara 'ksantelazma' "
            "(xanthelasma palpebrarum) adı verilir ve en sık görülen formdur.\n\n"
            "Diğer formlar arasında kalça ve dirseklerde tüböröz ksantomlar, gövdede erüptif ksantomlar ve ekstansör "
            "tendonlarda tendon ksantomları yer alır."
        ),
        "medicalTerms": [
            {"term": "Ksantom", "explanation": "Deri veya tendonlarda köpük makrofajların oluşturduğu sarı renkli lipid lezyonudur."},
            {"term": "Ksantelazma", "explanation": "Göz kapağı derisinde kolesterol yüklü köpüksü histiositlerin oluşturduğu sarı plaklardır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Ksantomlar neoplazi değildir; kolesterol yüklü makrofajların fokal birikimidir.",
            "📌 [SINAV SPOTU] Ksantelazma göz kapağında yerleşen en sık kutanöz ksantom tipidir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Doku Tutulumu", "desc": "Dermis, subkutanöz doku ve tendon kılıfları.", "isKey": True},
                {"title": "Hücresel İçerik", "desc": "Kolesteril ester zengini köpük histiositler (Touton dev hücreleri).", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Göz kapağı derisinde kolesterol birikimiyle karakterize sarımsı plaklara ksantelazma adı verilir.",
                "ksantelazma",
                "Göz kapağında görülen fokal lipid plağı"
            ),
            make_active_recall(
                "Ksantomların mikroskobik incelemesinde baskın olarak izlenen hücresel yapı nedir?",
                "Sitoplazması kolesterol ve kolesteril ester dolu vakuollü makrofajlar (köpük hücreler) ve bazen Touton dev hücreleridir."
            )
        ]
    })

    # ADIM 27
    slides.append({
        "slideNumber": 27,
        "title": "Ailesel Hiperkolesterolemi ve Aşil Tendonu Ksantomlarının Önemi",
        "subtitle": "LDL reseptör mutasyonu, erken koroner arter hastalığı ve patognomonik fizik muayene",
        "badge": "Genetik Hiperkolesterolemi",
        "badgeColor": "red",
        "synthesisNarrative": (
            "Ailesel hiperkolesterolemi (FH), LDL reseptör genindeki (LDLR) mutasyonlar nedeniyle plazma LDL klirensinin "
            "bozulduğu, otozomal dominant geçişli en önemli genetik metabolizma hastalığıdır. Heterozigotlarda LDL düzeyleri "
            "2-3 kat, homozigotlarda 5-6 kat artar. Bu hastalarda henüz 30'lu yaşlarda (homozigotlarda çocuklukta) miyokard "
            "enfarktüsü gelişme riski taşır.\n\n"
            "> [SINAV SPOTU] Aşil tendonu ksantomları, ailesel hiperkolesteroleminin neredeyse patognomonik klinik fizik "
            "muayene bulgusudur; tendon kılıfında kolesterol yüklü histiositler nodüler kitleler oluşturur.\n\n"
            "Aşil tendonunda kalınlaşma veya nodül saptanan genç bir hastada mutlaka lipit profili ve genetik tarama yapılmalıdır."
        ),
        "medicalTerms": [
            {"term": "Ailesel Hiperkolesterolemi", "explanation": "LDL reseptör mutasyonuna bağlı şiddetli hiperkolesterolemi ve erken ateroskleroz hastalığıdır."},
            {"term": "Tendon Ksantomu", "explanation": "Özellikle Aşil ve el ekstansör tendonlarında gelişen sert nodüler kolesterol kitleleridir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Aşil tendonu ksantomu ailesel hiperkolesterolemi için son derece karakteristik bir bulgudur.",
            "📌 [SINAV SPOTU] LDL reseptör defekti karaciğerin kandan LDL'yi temizlemesini engeller."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Moleküler Defekt", "desc": "LDL reseptör kaybı veya işlev bozukluğu.", "isKey": True},
                {"title": "Klinik İpuçları", "desc": "Aşil ksantomu, kornea arkusu ve erken koroner arter hastalığı.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_micro_quiz(
                "28 yaşında bir erkek hasta topuk arkasında ağrısız sert nodüler şişlik şikayetiyle başvuruyor. Fizik muayenede Aşil tendonunda nodüler kalınlaşma ve korneal arkus izleniyor. Biyopside köpüklü histiosit kümeleri saptanıyor. Bu hastada öncelikle hangi genetik defekt düşünülmelidir?",
                {
                    "A": "CFTR geni klor kanal mutasyonu",
                    "B": "LDL reseptör gen mutasyonuna bağlı ailesel hiperkolesterolemi",
                    "C": "Heksozaminidaz A enzim eksikliği",
                    "D": "SERPINA1 geninde yanlış katlanma mutasyonu",
                    "E": "Glukoserebrozidaz enzim delesyonu"
                },
                "B",
                {
                    "A": "CFTR kistik fibrozise neden olur, tendon ksantomu yapmaz.",
                    "B": "Doğru! Aşil tendonu ksantomu ve korneal arkus ailesel hiperkolesteroleminin (LDL reseptör mutasyonu) klasik bulgusudur.",
                    "C": "Heksozaminidaz Tay-Sachs hastalığı etkenidir.",
                    "D": "SERPINA1 alfa-1 antitripsin eksikliği genidir.",
                    "E": "Glukoserebrozidaz Gaucher hastalığıyla ilgilidir."
                }
            ),
            make_cloze(
                "Ailesel hiperkolesterolemi hastalarında Aşil tendonu kılıfında karakteristik kolesterol yüklü tendon ksantomları gelişir.",
                "tendon ksantomları",
                "Tendonlarda kolesterol birikimiyle oluşan nodüller"
            )
        ]
    })

    # ADIM 28
    slides.append({
        "slideNumber": 28,
        "title": "Kolesterolozis (Çilek Safra Kesesi): Lamina Propriada Köpük Hücreler",
        "subtitle": "Safra kesesi mukozasında kolesterol emilimi ve çilek manzarası",
        "badge": "Kolesterolozis",
        "badgeColor": "cyan",
        "synthesisNarrative": (
            "Kolesterolozis, safra kesesi mukozasının lamina propria tabakasında kolesterol yüklü köpüksü makrofajların "
            "fokal veya diffüz birikimiyle karakterize benign bir durumdur. Safradaki aşırı kolesterol konsantrasyonu "
            "epitelden lamina propriaya emilir ve burada yerleşik histiositler tarafından fagosite edilir.\n\n"
            "> [SINAV SPOTU] Makroskopik incelemede parlak kırmızı hiperemik safra kesesi mukozası üzerinde benek benek "
            "dizilmiş sarı lipid lekeleri taze bir çileği andırdığı için 'çilek safra kesesi' (strawberry gallbladder) adını alır.\n\n"
            "Bu durum genellikle asemptomatiktir; ancak bazen makrofaj kümeleri polipoid çıkıntılar (kolesterol polipleri) "
            "oluşturabilir ve kolesistektomi materyalinde tesadüfen saptanır."
        ),
        "medicalTerms": [
            {"term": "Kolesterolozis", "explanation": "Safra kesesi lamina propriasında köpüklü histiositlerin kolesterol depolamasıdır."},
            {"term": "Çilek Safra Kesesi", "explanation": "Kırmızı mukoza üzerindeki sarı kolesterol beneklerinin oluşturduğu makroskobik görünümdür."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Çilek safra kesesi lamina propriada kolesterol yüklü makrofaj birikimini ifade eder.",
            "📌 [SINAV SPOTU] Histolojide epitel normaldir; kolesterol birikimi lamina propriadaki köpük hücrelerdedir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Lokalizasyon", "desc": "Safra kesesi lamina propria tabakası (epitel değil).", "isKey": True},
                {"title": "Makroskopi", "desc": "Kırmızı mukoza zemininde küçük sarı lipid benekleri.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "Ateroskleroz vs Kolesterolozis",
                "Ateroskleroz (Damar Duvarı)",
                "Büyük arterlerin intimasında köpük hücreler, ekstraselüler kristaller ve lümeni daraltan fibröz şapka içerir.",
                "Kolesterolozis (Safra Kesesi)",
                "Safra kesesi lamina propriasında epitel altında toplanan köpük histiositler içerir; lümeni tıkamaz, sarı benekler yapar."
            ),
            make_active_recall(
                "Çilek safra kesesi tablosunda köpük hücreler safra kesesi duvarının tam olarak hangi histolojik katmanında yerleşir?",
                "Mukozanın lamina propria (subepitelyal bağ dokusu) tabakasında yerleşir."
            )
        ]
    })

    # ADIM 29 - CHECKPOINT 3
    slides.append({
        "slideNumber": 29,
        "title": "[TEKRAR SAYFASI - CHECKPOINT 3] Kolesterol Birikimleri ve Klinik Tablolar",
        "subtitle": "Köpük hücreler, ateroskleroz, ksantomlar ve çilek safra kesesinin sentezi",
        "badge": "Checkpoint",
        "badgeColor": "red",
        "isCheckpoint": True,
        "checkpointNumber": 3,
        "synthesisNarrative": (
            "Bu checkpoint sayfasında kolesterol ve kolesteril ester birikimlerinin hücresel biyolojisini ve klinik "
            "antitisini sentezliyoruz. Kolesterol yıkılamayan bir steroldür; fazlası hücrede vakuollerde ester olarak depolanır "
            "veya kristalleşir. Makrofajlar oxLDL'yi çöpçü reseptörlerle geri bildirimsiz yutarak köpük hücrelere dönüşür.\n\n"
            "> [YÜKSEK VERİM] Aterosklerozda intimal plaklar ve kolesterol kristalleri, ksantomlarda deri/tendon lezyonları "
            "(özellikle Aşil ksantomu), safra kesesinde ise lamina propriada çilek safra kesesi meydana gelir.\n\n"
            "Aşağıdaki 3 akıl kartını dikkatle gözden geçirerek kolesterol patolojilerini zihninize mühürleyiniz."
        ),
        "medicalTerms": [
            {"term": "Köpük Hücre", "explanation": "Kolesteril ester damlalarıyla sitoplazması köpüksü görünen histiosit veya düz kas hücresidir."},
            {"term": "Çilek Safra Kesesi", "explanation": "Safra kesesi lamina propriasında kolesterolozis lezyonunun makroskobik adıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Aşil tendonu ksantomu ailesel hiperkolesterolemiyi düşündürür.",
            "📌 [SINAV SPOTU] Rutin kesitlerde kolesterol eridiği için köpüksü vakuoller ve iğsi yarıklar kalır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Köpük Hücre Biyolojisi", "desc": "Çöpçü reseptörler aracılığıyla sınırsız oxLDL alımı.", "isKey": True},
                {"title": "Organ Manifestasyonları", "desc": "Arter intimasında plak, deride ksantom, safra kesesinde çilek mukoza.", "isKey": True}
            ]
        },
        "flashcards": [
            make_flashcard(
                "k1-07-fc-07",
                "Köpük hücrelerin (foam cells) histolojik kesitlerde sitoplazmalarının boş ve köpüksü görünmesinin nedeni nedir?",
                "Doku takibi sırasında kullanılan organik çözücülerin (alkol ve ksilol) hücre içindeki kolesteril ester damlacıklarını eritmesidir.",
                "Rutin histoteknolojik fiksasyon ve lipid erimesi"
            ),
            make_flashcard(
                "k1-07-fc-08",
                "Aşil tendonu ksantomu hangi genetik metabolizma hastalığı için karakteristik bir bulgudur?",
                "LDL reseptör mutasyonu sonucu gelişen ailesel hiperkolesterolemi için karakteristiktir.",
                "Tendon tutulumu ve ailesel hiperlipidemi"
            ),
            make_flashcard(
                "k1-07-fc-09",
                "Çilek safra kesesi (kolesterolozis) patolojisinde lipid yüklü makrofajlar duvarın hangi tabakasında birikir?",
                "Safra kesesi mukozasının lamina propria tabakasında birikir.",
                "Safra kesesi histolojisi ve subepitelyal tutulum"
            )
        ],
        "interactiveElements": [
            make_cloze(
                "Ateromatöz plakların nekrotik merkezinde eriyen kolesterol kristalleri mikroskopta iğsi kolesterol kristalleri şeklinde yarıklar bırakır.",
                "kolesterol kristalleri",
                "Nekrotik merkezde çöken serbest sterol yapıları"
            )
        ]
    })

    # ADIM 30
    slides.append({
        "slideNumber": 30,
        "title": "Ateroskleroz ve Ksantomların Karşılaştırmalı Ayırıcı Tanısı",
        "subtitle": "Klinik senaryolarda lipid birikim paternlerinin ayırt edilmesi",
        "badge": "Ayırıcı Tanı",
        "badgeColor": "emerald",
        "synthesisNarrative": (
            "Klinik patolojide kolesterol depolanmaları incelenirken hastanın yaşı, genetik öyküsü, tutulan anatomik lokalizasyon "
            "ve lezyonun mikroskobik mimarisi entegre edilir. Damar intimasındaki köpük hücreler iskemi ve enfarkt riski taşırken, "
            "derideki ksantomlar altta yatan sistemik dislipideminin habercisidir.\n\n"
            "> [KLİNİK İPUCU] Ksantelazması olan hastaların yaklaşık yarısında serum lipidleri normal bulunabilir; oysa "
            "tüberöz ve tendon ksantomları daima ağır genetik hiperkolesterolemiyi belgeler.\n\n"
            "Patolog biyopsi materyalinde köpüksü hücre gördüğünde steatoz (trigliserid), ksantom (kolesterol) ve lizozomal "
            "depo hastalıkları arasında histokimyasal ve klinik korelasyon kurmalıdır."
        ),
        "medicalTerms": [
            {"term": "Dislipidemi", "explanation": "Serum kolesterol, trigliserid veya lipoprotein düzeylerinin anormal dağılımıdır."},
            {"term": "Ksantelazma Palpebrarum", "explanation": "Göz kapağında yerleşen, normolipidemik kişilerde de görülebilen fokal lezyondur."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Ksantelazma normolipidemik bireylerde de görülebilir; tendon ksantomu ise ağır hiperkolesterolemi işaretidir.",
            "📌 [SINAV SPOTU] Damar duvarı lezyonlarında köpük hücrelere fibröz kapsül ve nekrotik çekirdek eşlik eder."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Damar vs Kutanöz", "desc": "Arterde trombofilik risk, deride kozmetik/tanısal gösterge.", "isKey": True},
                {"title": "Laboratuvar Bağı", "desc": "Aşil ksantomunda LDL tavan yapar, ksantelazmada normal olabilir.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_branching_logic(
                "35 yaşında ani göğüs ağrısıyla başvuran bir hastada koroner anjiyografide LAD arterinde tam tıkanıklık saptanıyor. Fizik muayenede her iki Aşil tendonunda nodüler kitleler fark ediliyor. En olası tanı ve mekanizma nedir?",
                [
                    {
                        "text": "Sigaraya bağlı endotel hasarı ve basit antrakozis birikimi",
                        "isCorrect": False,
                        "feedback": "Antrakozis akciğerde karbon birikimidir, Aşil nodülü ve erken koroner tıkanıklığı açıklamaz."
                    },
                    {
                        "text": "Ailesel hiperkolesterolemiye bağlı tendon ksantomları ve erken agresif koroner ateroskleroz",
                        "isCorrect": True,
                        "feedback": "Doğru teşhis! Genç yaşta Aşil tendon ksantomu ve miyokard enfarktüsü birlikteliği ailesel hiperkolesteroleminin klasik tablosudur."
                    }
                ]
            ),
            make_active_recall(
                "Ksantelazma ile Aşil tendonu ksantomunun serum lipid düzeyleriyle ilişkisi açısından farkı nedir?",
                "Ksantelazma normolipidemik kişilerde de görülebilirken, Aşil tendonu ksantomu hemen daima ağır ailesel hiperkolesterolemi ile birliktedir."
            )
        ]
    })

    return slides
