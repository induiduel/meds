"""
Bölüm 6: Makrobesinler (Protein, DHA/Omega-3) ve Esansiyel Mikrobesinler (Kalsiyum, Çinko, İyot, A, C, B12)
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
        "title": "Gebelikte Protein Gereksinimi: Toplam 925 g ve Günlük +20-25 g",
        "subtitle": "Fetüs, plasenta, uterus ve eritrosit kütlesi için yapı taşı sentezi",
        "badge": "Protein Dengesi",
        "badgeColor": "emerald",
        "synthesisNarrative": (
            "Proteinler, gebelikte hızla bölünen fetal hücrelerin, genişleyen plasenta dokusunun, hipertrofiye uğrayan uterus kaslarının "
            "ve artan maternal eritrosit kitlesinin temel yapı taşıdır. Tüm gebelik boyunca maternal ve fetal dokularda depolanan "
            "toplam net protein miktarı ortalama 925 gramdır.\n\n"
            "> [SINAV SPOTU] Gebelik boyunca fetüs, plasenta ve dokular için ortalama 925 g protein gerekir; proteinin biyolojik "
            "kalitesi ve sindirilebilirliği dikkate alınarak gebenin günlük diyetine 20 - 25 G EK PROTEİN eklenmelidir.\n\n"
            "Bu ek proteinin en az yarısı biyolojik değeri yüksek (elzem aminoasitleri tam içeren) yumurta, süt, et ve balık gibi hayvansal "
            "kaynaklardan veya dengeli kuru baklagil-tahıl kombinasyonlarından sağlanmalıdır."
        ),
        "medicalTerms": [
            {"term": "Net Protein Depolanması", "explanation": "Gebelikte yeni oluşan fötal ve maternal dokularda biriken toplam 925 gramlık aminoasit havuzudur."},
            {"term": "Biyolojik Değeri Yüksek Protein", "explanation": "İnsan vücudunun sentezleyemediği elzem aminoasitleri eksiksiz ve dengeli içeren protein türüdür (özellikle yumurta)."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Gebelik boyunca depolanan toplam protein: ortalama 925 g.",
            "📌 [SINAV SPOTU] Gebelikte günlük diyete eklenmesi gereken protein miktarı: 20 - 25 g.",
            "📌 [SINAV SPOTU] Örnek protein yumurta olup anne ve fötal doku sentezinde altın standarttır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Toplam 925 g", "desc": "Fetüs, plasenta ve maternal organlarda biriken toplam protein miktarıdır.", "isKey": True},
                {"title": "Günlük +20-25 g", "desc": "Kalite faktörüyle birlikte günlük diyete eklenmesi gereken proteindir.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Gebelikte doku sentezi ve fötal büyüme için gebenin günlük diyetine 20-25 g ek protein ilave edilmelidir.",
                "20-25 g",
                "Günlük diyete eklenecek protein miktarı"
            ),
            make_active_recall(
                "Gebelikte toplam depolanan protein miktarı ve günlük diyete eklenmesi gereken ilave protein miktarı ne kadardır?",
                "Gebelik boyunca toplam ortalama 925 g protein depolanır; sindirilebilirlik ve kalite düşünülerek günlük diyete 20 - 25 g ek protein eklenmelidir."
            )
        ]
    })

    # ADIM 52
    slides.append({
        "slideNumber": 52,
        "title": "Yağlar ve Esansiyel Yağ Asitleri: Fetal Beyin ve DHA (n-3)",
        "subtitle": "Kuru beyin kütlesinin %50-60'ı yağ; dokosahekzaenoik asit ve retina fotoreseptörleri",
        "badge": "Esansiyel Yağlar",
        "badgeColor": "blue",
        "synthesisNarrative": (
            "Lipitler yalnızca yoğun bir enerji kaynağı değil, aynı zamanda hücre membranlarının ve santral sinir sisteminin temel yapısal "
            "bileşenidir. İnsan beyninin kuru katı ağırlığının yaklaşık %50-60'ı yağlardan oluşur. Özellikle üçüncü trimestrde hızlanan "
            "fötal beyin korteksi büyümesinde ve retina fotoreseptör tabakasının yapılanmasında Dokosahekzaenoik Asit (DHA, 22:6 n-3) "
            "vazgeçilmez bir esansiyel rol oynar.\n\n"
            "> [SINAV SPOTU] Fötal beyin ve sinir dokusunun katı kısmının %50-60'ı yağdır; özellikle DHA (omega-3) nöral gelişim "
            "ve görme keskinliği için kritiktir. Temel kaynaklar: yağlı balıklar, ceviz, keten tohumu ve kanola yağıdır.\n\n"
            "Annenin diyetle yeterli n-3 çoklu doymamış yağ asidi (PUFA) alması, bebekte nörobilişsel skorları artırırken aynı zamanda "
            "maternal preeklampsi ve erken doğum riskini de azaltmaktadır."
        ),
        "medicalTerms": [
            {"term": "Dokosahekzaenoik Asit (DHA)", "explanation": "Beyin korteksi ve retinada en yoğun bulunan, fetal nöronal membran akışkanlığını sağlayan n-3 yağ asididir."},
            {"term": "Retinal Fotoreseptör Diski", "explanation": "Görme sinyalini başlatan ve rodopsin fonksiyonu için yüksek oranda DHA içeren retina zarlarıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Fetal beynin katı kısmının %50-60'ı yağdır.",
            "📌 [SINAV SPOTU] DHA (omega-3) fötal beyin ve retina gelişimi için elzemdir; kaynak: yağlı balık, ceviz, kanola yağı.",
            "📌 [SINAV SPOTU] Derin dip balıklarında metil cıva riski olduğundan hamsi, sardalya ve somon tercih edilmelidir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Beynin %50-60'ı Yağ", "desc": "Nöron akson miyelinizasyonu ve membranlar lipid zenginidir.", "isKey": True},
                {"title": "DHA Kritikliği", "desc": "Retina görme fonksiyonu ve kortikal sinaps oluşumunda başroldedir.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Fötal beyin ve retina gelişimi için elzem olan n-3 serisi uzun zincirli yağ asidine DHA adı verilir.",
                "DHA",
                "Dokosahekzaenoik asit kısaltması"
            ),
            make_active_recall(
                "Fetal beyin gelişimi açısından yağların önemi nedir ve DHA hangi besin kaynaklarından sağlanır?",
                "Beynin katı kısmının %50-60'ı yağdır; DHA nörogenez ve retina için elzemdir. Başlıca kaynakları yağlı balıklar, ceviz, soya fasulyesi ve kanola yağıdır."
            )
        ]
    })

    # ADIM 53
    slides.append({
        "slideNumber": 53,
        "title": "Kalsiyum Metabolizması: Günlük 1000-1300 mg Hedefi",
        "subtitle": "Fetal iskelet mineralizasyonu (30 g kalsiyum) ve maternal osteoporoz profilaksisi",
        "badge": "Kalsiyum",
        "badgeColor": "emerald",
        "synthesisNarrative": (
            "Gebelikte fetüs, term dönemine ulaştığında tam mineralize olmuş bir iskelet yapısına kavuşabilmek için anneden aktif "
            "plasental transferle yaklaşık 30 gram saf elementer kalsiyum çeker. Bu transferin yaklaşık %80'i kemik mineralizasyonunun "
            "zirve yaptığı üçüncü trimestrde gerçekleşir. Annenin diyetinde yeterli kalsiyum bulunmadığında fötal gereksinim annenin "
            "kendi trabeküler kemiklerinden kalsiyum rezorpsiyonu ile karşılanır.\n\n"
            "> [SINAV SPOTU] Gebelikte kalsiyum ihtiyacı günlük 1000 - 1300 mg'dır (özellikle adolesan gebelerde 1300 mg). Bir su bardağı "
            "(240 g) süt veya yoğurt yaklaşık 300 mg kalsiyum sağlar. Yeterli alım anneyi ilerideki osteoporozdan korur.\n\n"
            "Aynı zamanda yeterli kalsiyum alımı paratiroid hormonu ve kalsitriol düzeylerini baskılayarak vasküler düz kas tonusunu "
            "düşürür ve preeklampsi gelişme riskini %35-50 oranında azaltır."
        ),
        "medicalTerms": [
            {"term": "Fetal Kalsiyum Çekimi", "explanation": "Terme kadar fötal iskelete anneden aktarılan yaklaşık 30 gram kalsiyumdur."},
            {"term": "Aktif Kalsiyum Transportu", "explanation": "Plasentada fötal dolaşıma karşı kalsiyum pompalayan Ca-ATPaz bağımlı mekanizmadır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Gebelikte günlük kalsiyum gereksinimi: 1000 - 1300 mg (adolesan gebede 1300 mg).",
            "📌 [SINAV SPOTU] 240 g süt veya yoğurt yaklaşık 300 mg kalsiyum içerir.",
            "📌 [SINAV SPOTU] Kalsiyum desteği preeklampsi riskini azaltmada kanıta dayalı bir halk sağlığı stratejisidir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "1000 - 1300 mg", "desc": "Gebelikte hedeflenen günlük elementer kalsiyum miktarıdır.", "isKey": True},
                {"title": "Adolesanda 1300 mg", "desc": "Kendi kemik kütlesi gelişen adölesan anneye üst doz verilir.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Gebelikte hem fetüsün iskeletini kurmak hem de anneyi osteoporozdan korumak için günlük 1000-1300 mg kalsiyum önerilir.",
                "1000-1300 mg",
                "Günlük kalsiyum alım aralığı"
            ),
            make_active_recall(
                "Gebelikte kalsiyum ihtiyacı günlük ne kadardır ve adolesan gebelerde bu hedef neden 1300 mg'a yükselir?",
                "Yetişkin gebede 1000 mg, adolesan gebede 1300 mg'dır. Adolesan annenin kendi doruk kemik kütlesine ulaşması için ek kalsiyuma gereksinimi vardır."
            )
        ]
    })

    # ADIM 54
    slides.append({
        "slideNumber": 54,
        "title": "Çinko (Zn) Esansiyelliği ve Fitat Etkileşimi",
        "subtitle": "DNA/RNA polimeraz kofaktörü, intrauterin büyüme ve emilim engelleri",
        "badge": "Çinko",
        "badgeColor": "amber",
        "synthesisNarrative": (
            "Çinko, vücutta 300'den fazla enzimin (özellikle DNA polimeraz, RNA polimeraz, alkalen fosfataz) ve çinko-parmak "
            "transkripsiyon faktörlerinin katalitik ve yapısal merkezinde yer alan hayati bir eser elementtir. Fötal hücre proliferasyonu, "
            "protein sentezi ve bağışıklık sistemi olgunlaşması doğrudan çinko yeterliliğine bağlıdır.\n\n"
            "> [SINAV SPOTU] Çinko eksikliği; intrauterin büyüme geriliği (IUGR), konjenital anomaliler, erken doğum ve ölü doğum "
            "riskini belirgin artırır. Tahıllardaki FİTATLAR çinkoyu bağlayarak bağırsaktan emilimini engeller!\n\n"
            "Mayalanmamış tam buğday ekmeği ve kepekli tahıllar yüksek miktarda fitat içerir; geleneksel mayalama (fermantasyon) işlemi "
            "fitaz enzimini aktive ederek çinkonun biyoyararlanımını artırır. Et ve deniz ürünleri en zengin çinko depolarıdır."
        ),
        "medicalTerms": [
            {"term": "Fitat (Fitik Asit)", "explanation": "Tahıl ve baklagillerde bulunan, çinko ve demiri çökelterek emilimlerini bloke eden antinütrienttir."},
            {"term": "Çinko-Parmak Motifi", "explanation": "DNA'ya bağlanarak fetal organogenez genlerinin ifadesini kontrol eden çinko bağımlı protein yapısıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Çinko eksikliği: IUGR, ölü doğum ve konjenital anomali riskini artırır.",
            "📌 [SINAV SPOTU] Tahıllardaki fitatlar çinko ve demir emilimini engeller; mayalı ekmek tüketimi bu engeli çözer."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "IUGR Tehdidi", "desc": "Çinko açığı fötal boy ve kilo kazanımını doğrudan frenler.", "isKey": True},
                {"title": "Fitat Blokajı", "desc": "Kepekli mayasız tahıllar çinko emilimini bağırsağa hapseder.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Kepekli tahıllarda bulunan ve çinko ile demir emilimini engelleyen antinütrient maddeye fitat adı verilir.",
                "fitat",
                "Tahıllardaki mineral bağlayıcı asit"
            ),
            make_active_recall(
                "Gebelikte çinko eksikliğinin fetüs üzerindeki 3 majör klinik sonucu nedir ve çinko emilimini bozan diyet bileşeni hangisidir?",
                "Sonuçlar: İntrauterin büyüme geriliği (IUGR), ölü doğum ve doğumsal anomali artışıdır. Emilimi engelleyen diyet bileşeni tahıllardaki fitatlardır."
            )
        ]
    })

    # ADIM 55
    slides.append({
        "slideNumber": 55,
        "title": "İyot Yetersizliği Bozuklukları: Kretenizm ve Zeka Geriliği",
        "subtitle": "Fetal nörolojik kretinism, sağırlık, cücelik ve endemik guatr",
        "badge": "İyot",
        "badgeColor": "red",
        "synthesisNarrative": (
            "İyot, maternal ve fetal tiroid hormonlarının (T3 ve T4) sentezlenmesi için zorunlu olan tek mineraldir. Fötal tiroid "
            "bezi 12. gebelik haftasına kadar hormon üretemez; bu kritik ilk trimester evresinde fetal beyin korteksi, serebellum "
            "ve kokleanın nöronal göçü tamamen anneden plasenta yoluyla geçen tiroksine (T4) muhtaçtır.\n\n"
            "> [SINAV SPOTU] İyot eksikliği annede guatr, düşük ve ölü doğuma; bebekte ise KRETENİZM (ağır zeka geriliği, sağırlık-dilsizlik, "
            "cücelik, spastisite) ve neonatal hipotiroidiye yol açar. Önlenebilir zeka geriliğinin dünyadaki bir numaralı nedenidir!\n\n"
            "Tüm bu dramatik tabloyu önlemenin en basit, en ucuz ve en etkili halk sağlığı aracı toplum genelinde iyotlu tuz kullanımıdır."
        ),
        "medicalTerms": [
            {"term": "Nörolojik Kretenizm", "explanation": "Erken gebelikte ağır iyot eksikliğine bağlı derin zeka geriliği, sağırlık-dilsizlik ve spastik diplejidir."},
            {"term": "Endemik Guatr", "explanation": "Toprağında ve suyunda iyot bulunmayan coğrafyalarda TSH uyarısıyla tiroid bezinin büyümesidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] İyot eksikliği: Dünyada önlenebilir zeka geriliği ve kretenizmin en sık nedenidir.",
            "📌 [SINAV SPOTU] Fetal sonuçlar: Zeka geriliği, sağırlık, cücelik, hipotiroidi; maternal sonuç: Düşük, ölü doğum, guatr.",
            "📌 [SINAV SPOTU] En kolay ve ucuz önleme yolu: İyotlu tuz kullanımıdır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Kretenizm Riski", "desc": "Derin zihinsel retardasyon ve işitme kaybıyla seyreden konjenital tablodur.", "isKey": True},
                {"title": "İyotlu Tuz Çözümü", "desc": "Toplumsal tuz zenginleştirmesi kretinizmi sıfırlayan halk sağlığı zaferidir.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Gebelikte ağır iyot eksikliği sonucu bebekte geri dönüşsüz zeka geriliği, sağırlık ve cücelikle seyreden kretenizm gelişir.",
                "kretenizm",
                "Konjenital tiroid ve iyot eksikliği sendromu"
            ),
            make_active_recall(
                "Gebelikte iyot eksikliğinin anne ve bebek üzerindeki majör klinik sonuçları nelerdir?",
                "Annede düşük, ölü doğum ve guatr; bebekte kretenizm (ağır zeka geriliği, cücelik, sağırlık-dilsizlik) ve hipotiroididir."
            )
        ]
    })

    # ADIM 56
    slides.append({
        "slideNumber": 56,
        "title": "İyotlu Tuzun Doğru Saklanması ve Tüketim İlkeleri",
        "subtitle": "Koyu renkli, ağzı kapalı, nemsiz ortam ve yemek piştikten sonra ekleme",
        "badge": "İyotlu Tuz",
        "badgeColor": "emerald",
        "synthesisNarrative": (
            "İyotlu tuz tüketimi gebelikte kretinizmi önlemede hayati olmakla birlikte, iyot kimyasal yapısı gereği (potasyum iyodat/iyodür) "
            "ışık, ısı ve nem karşısında son derece uçucu (sublime olan) ve kararsız bir bileşiktir. Yanlış saklanan ve pişirilen tuz "
            "iyodunu tamamen kaybeder.\n\n"
            "> [SINAV SPOTU] İyotlu tuz; ışık ve güneş görmeyen, nemsiz ortamda, KOYU RENKLİ ve AĞZI KAPALI kaplarda saklanmalıdır. "
            "Yemek pişerken değil, yemek piştikten sonra veya sofrada eklenmelidir (ısı iyodu uçurur)!\n\n"
            "Tuzun şeffaf tuzluklarda güneş altında tutulması veya kaynayan tencereye ilk başta atılması iyot içeriğinin %60-80'inin "
            "buharlaşarak yok olmasına neden olur."
        ),
        "medicalTerms": [
            {"term": "İyot Uçuculuğu", "explanation": "İyot tuzlarının yüksek sıcaklık, UV ışını ve rutubette gaz haline geçerek tuzdan ayrılmasıdır."},
            {"term": "Koyu Renkli Saklama Kabı", "explanation": "İyodu fotooksidasyondan koruyan opakt cam veya porselen muhafaza kabıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] İyotlu tuz: Koyu renkli, ağzı kapalı kapta, nemsiz ve ışıksız ortamda saklanmalıdır.",
            "📌 [SINAV SPOTU] İyot ısıya duyarlıdır; yemek pişerken değil ateşten alındıktan sonra eklenmelidir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Koyu Kapta Saklama", "desc": "Işık ve nem iyodu parçaladığı için opak kap şarttır.", "isKey": True},
                {"title": "Ateşten Sonra Ekleme", "desc": "Yüksek kaynama sıcaklığı iyot gazını buharlaştırır.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "İyotlu tuzun içindeki iyodun buharlaşıp kaybolmaması için mutlaka koyu renkli ve ağzı kapalı kapta saklanması gerekir.",
                "koyu renkli",
                "Işıktan koruyan saklama kabı özelliği"
            ),
            make_active_recall(
                "İyotlu tuzun biyoaktif iyot içeriğini korumak için saklama koşulları ve yemeklere eklenme zamanlaması nasıl olmalıdır?",
                "Işık ve güneş görmeyen, nemsiz ortamda, koyu renkli ve ağzı kapalı kapta saklanmalıdır; yemek pişerken değil, piştikten sonra (ateşten indirilirken) eklenmelidir."
            )
        ]
    })

    # ADIM 57
    slides.append({
        "slideNumber": 57,
        "title": "A Vitamini Dengesi: Fetal İhtiyaç vs Teratojenite Riski",
        "subtitle": "Eksiklikte prematürite ve körlük; fazlasında yarık damak ve kardiyak malformasyonlar",
        "badge": "A Vitamini",
        "badgeColor": "red",
        "synthesisNarrative": (
            "A vitamini (retinol ve beta-karoten), gebelikte embriyonik kalp, göz, kulak ve ekstremite gelişiminde morfogenetik bir "
            "düzenleyicidir. A vitamini eksikliği gelişmekte olan ülkelerde prematürite, düşük doğum ağırlığı, mikrosefali ve neonatal "
            "görme kusurlarına yol açar. Ancak A vitamininin fazlası eksikliğinden çok daha ölümcüldür.\n\n"
            "> [SINAV SPOTU] A vitamininin yüksek dozu (özellikle >10.000 IU/gün veya izotretinoin) KESİNLİKLE TERATOJENİKTİR! "
            "Spontan abortus, kraniyofasiyal malformasyonlar (yarık damak-dudak), timus agenezisi ve konjenital kalp defektlerine yol açar.\n\n"
            "Bu nedenle gebelere asla yüksek doz preforme A vitamini (retinol) veya karaciğer gibi zengin sakatatlar verilmemeli; "
            "ihtiyaç teratojenik riski olmayan bitkisel beta-karoten kaynaklarından karşılanmalıdır."
        ),
        "medicalTerms": [
            {"term": "Retinoik Asit Embriyopatisi", "explanation": "Yüksek doz A vitamini/izotretinoinin nöral krest göçünü bozarak kraniofasiyal ve kardiyak anomaliler yapmasıdır."},
            {"term": "Beta-Karoten", "explanation": "Vücudun ihtiyaca göre retinole dönüştürdüğü, toksisite ve teratojenite riski taşımayan provitamin A formudur."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] A vitamini fazlası KESİNLİKLE TERATOJENİKTİR (yarık damak, kalp anomalileri, spontan abortus).",
            "📌 [SINAV SPOTU] Akne tedavisinde kullanılan retinoidler (izotretinoin) gebelikte mutlak kontrendikedir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Teratojenik Doz", "desc": "Preforme retinol aşırılığı nöral krest hücrelerini parçalar.", "isKey": True},
                {"title": "Yarık Damak ve Kalp", "desc": "A vitamini fazlalığının en tipik konjenital malformasyonlarıdır.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Gebelikte yüksek dozda alınan preforme A vitamini nöral krest hasarı yaratarak yarık damak gibi teratojenik anomalilere yol açar.",
                "yarık damak",
                "A vitamini fazlalığında gelişen kraniofasiyal anomali"
            ),
            make_active_recall(
                "Gebelikte A vitamininin eksikliği ve fazlalığı hangi majör komplikasyonlara yol açar?",
                "Eksikliği prematürite, DDA, mikrosefali ve görme kusurları yapar; fazlalığı ise kesinlikle teratojeniktir (spontan düşük, yarık damak/dudak, konjenital kalp hastalıkları)."
            )
        ]
    })

    # ADIM 58
    slides.append({
        "slideNumber": 58,
        "title": "B12 Vitamini ve C Vitamini: Nöral Gelişim ve Kollajen",
        "subtitle": "Vejetaryen gebelerde B12 riski ve C vitamini ile demir emilim sinerjisi",
        "badge": "B12 ve C Vitamini",
        "badgeColor": "emerald",
        "synthesisNarrative": (
            "B12 vitamini (kobalamin), DNA sentezi, miyelin kılıf oluşumu ve folat metabolizmasının (metil kapanı) ayrılmaz bir "
            "ortağıdır. B12 vitamini doğada yalnız hayvansal kaynaklı besinlerde (et, süt, yumurta, balık) sentezlenir ve bulunur. "
            "Bu nedenle katı vegan veya vejetaryen beslenen gebe kadınlar ve bebekleri ağır bir B12 eksikliği tehdidi altındadır.\n\n"
            "> [SINAV SPOTU] B12 eksikliği annede ve bebekte MEGALOBLASTİK ANEMİ, nöral tüp defektleri ve kalıcı santral sinir "
            "sistemi hasarına yol açar; vejetaryen annelere mutlaka B12 desteği verilmelidir. C vitamini ise günlük +10 mg artırılır.\n\n"
            "C vitamini (askorbik asit); fötal kemik ve kıkırdak kollajen sentezinde prolin ve lizinin hidroksilasyonu için kofaktördür. "
            "Aynı zamanda bitkisel ferrik demiri (Fe3+) absorbe edilebilir ferröz (Fe2+) demire indirgeyerek demir emilimini katlar."
        ),
        "medicalTerms": [
            {"term": "Metil Kapanı (Methyl Trap)", "explanation": "B12 eksikliğinde folatın metiltetrahidrofolat formunda kilitlenerek DNA sentezinin durmasıdır."},
            {"term": "Ferrik-Ferröz İndirgenmesi", "explanation": "C vitamininin demir emilimini artırmak için demiri Fe3+'ten Fe2+'ye indirgemesidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] B12 vitamini yalnızca hayvansal gıdalarda bulunur; vejetaryen gebelerde megaloblastik anemi riski yüksektir.",
            "📌 [SINAV SPOTU] C vitamini ihtiyacı günlük +10 mg artırılır; demir emilimini ve kollajen sentezini artırır."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Vejetaryen Riski", "desc": "Et ve süt tüketmeyen gebede B12 desteği zorunludur.", "isKey": True},
                {"title": "C Vitamini Desteği", "desc": "Günlük 10 mg artış demir biyoyararlanımını güvenceye alır.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "B12 vitamini yalnız hayvansal gıdalarda bulunduğu için katı vejetaryen gebelerde megaloblastik anemi riski yüksektir.",
                "megaloblastik anemi",
                "B12 ve folat eksikliğinde görülen anemi türü"
            ),
            make_active_recall(
                "Neden katı vejetaryen gebe kadınlar B12 eksikliği açısından yüksek risk taşır ve bu eksikliğin fötal sonucu nedir?",
                "B12 vitamini yalnız hayvansal besinlerde bulunur. Eksikliğinde fetüste megaloblastik anemi, nöral tüp defektleri ve kalıcı serebral demiyelinizasyon gelişir."
            )
        ]
    })

    # ADIM 59 [CHECKPOINT 6]
    slides.append({
        "slideNumber": 59,
        "title": "[TEKRAR SAYFASI - CHECKPOINT 6] Makro ve Mikrobesinler İstasyonu",
        "subtitle": "Protein, DHA, kalsiyum, çinko, iyot, A ve B12 vitaminlerinin sentezi",
        "badge": "Checkpoint",
        "badgeColor": "teal",
        "isCheckpoint": True,
        "checkpointNumber": 6,
        "synthesisNarrative": (
            "Bu istasyon; gebelikte protein ihtiyacını (toplam 925 g, günlük ek 20-25 g), kuru beynin %50-60'ını oluşturan yağlar ve "
            "DHA'nın (omega-3) önemini, kalsiyum hedefini (1000-1300 mg, süt/yoğurt porsiyonu ~300 mg), çinko eksikliğinin IUGR yapmasını "
            "ve fitat blokajını, iyot eksikliğinin kretenizm/zeka geriliği yapmasını ve iyotlu tuzun koyu kapta saklanmasını, A vitamininin "
            "yüksek dozunun teratojenitesini (yarık damak) ve vejetaryenlerde B12 takviyesini konsolide eder.\n\n"
            "> [YÜKSEK VERİM] Protein = +20-25 g/gün; DHA = beyin/retina; Kalsiyum = 1000-1300 mg; İyot = kretenizm önleme (koyu kap); "
            "A vitamini fazlası = teratojenik; B12 = vejetaryen riski."
        ),
        "medicalTerms": [
            {"term": "Mikrobesin Kritik Eşikleri", "explanation": "Kalsiyum 1000-1300 mg, ek protein 20-25 g, C vitamini +10 mg."},
            {"term": "Teratojenite vs Kretinizm", "explanation": "A vitamini fazlalığı malformasyon yaparken, iyot eksikliği kretenizm yapar."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Protein: Toplam 925 g, günlük ek 20-25 g.",
            "📌 [SINAV SPOTU] Kalsiyum: Günlük 1000-1300 mg (adolesanda 1300 mg); preeklampsi riskini azaltır.",
            "📌 [SINAV SPOTU] İyot: Eksikliği kretenizm ve zeka geriliği yapar; iyotlu tuz koyu renkli kapta saklanır.",
            "📌 [SINAV SPOTU] A vitamini fazlası TERATOJENİKTİR; B12 vejetaryenlerde mutlaka desteklenmelidir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Protein ve DHA", "desc": "Yapı taşları ve sinir sistemi membranları eksiksiz kurulur.", "isKey": True},
                {"title": "Mineraller", "desc": "Kalsiyum, çinko ve iyot iskelet ve nörolojik sağlığı korur.", "isKey": True},
                {"title": "Vitamin Dengesi", "desc": "A vitamini fazlalığından kaçınılır, B12 ve C vitamini desteklenir.", "isKey": True}
            ]
        },
        "flashcards": [
            make_flashcard(
                "fc-k1-06-16",
                "Gebelikte günlük diyete eklenmesi gereken protein miktarı ve toplam depolanan protein ne kadardır?",
                "Günlük diyete 20 - 25 g ek protein eklenmelidir; gebelik boyunca depolanan toplam miktar ortalama 925 gramdır.",
                "Protein ihtiyacı değerleri"
            ),
            make_flashcard(
                "fc-k1-06-17",
                "İyot eksikliğinin bebek üzerindeki en dramatik sonucu nedir ve iyotlu tuz nasıl saklanmalıdır?",
                "Bebekte kretenizm (ağır zeka geriliği, sağırlık, cücelik) yapar; iyotlu tuz ışık ve güneş almayan, nemsiz ortamda, koyu renkli ve ağzı kapalı kapta saklanmalıdır.",
                "İyot eksikliği ve tuz saklama"
            ),
            make_flashcard(
                "fc-k1-06-18",
                "Gebelikte A vitamininin fazlalığı neden tehlikelidir ve hangi konjenital anomalilere yol açar?",
                "Yüksek doz A vitamini kesinlikle teratojeniktir; spontan abortus, yarık damak/dudak, konjenital kalp defektleri ve kraniofasiyal anomalilere yol açar.",
                "A vitamini teratojenitesi"
            )
        ],
        "interactiveElements": [
            make_table(
                ["Besin Öğesi / Mineral", "Gebelikteki Temel Rolü", "Eksikliği veya Fazlalığının Riskleri"],
                [
                    [("Protein", False, ""), ("Fetal ve maternal doku sentezi (toplam 925 g)", False, ""), ("Günlük 20-25 g eklenmezse kas yıkımı ve IUGR", True, "Protein açığında fötal büyüme kısıtlılığı")],
                    [("İyot", False, ""), ("Tiroid hormonu ve fötal beyin korteksi gelişimi", False, ""), ("Kretenizm, sağırlık ve derin zeka geriliği", True, "İyot eksikliğinin ağır konjenital tablosu")],
                    [("A Vitamini", False, ""), ("Görme pigmentleri ve organogenez kontrolü", False, ""), ("Fazlası yarık damak ve teratojenite yapar", True, "A vitamini toksisitesinin fötal anomalisi")]
                ]
            )
        ]
    })

    # ADIM 60
    slides.append({
        "slideNumber": 60,
        "title": "Diyet Çeşitliliği ve Temel Besin Grubu Porsiyonları",
        "subtitle": "Süt ve ürünleri (3-4 porsiyon), et grubu (3 porsiyon), sebze ve meyve dengesi",
        "badge": "Porsiyon Rehberi",
        "badgeColor": "emerald",
        "synthesisNarrative": (
            "Gebelikte optimal besin ögesi örüntüsünü yakalamanın tek yolu gıda çeşitliliğidir. Beslenme kılavuzları besinleri "
            "dört ana grupta toplar: 1) Süt ve ürünleri, 2) Et, yumurta ve kuru baklagiller, 3) Taze sebze ve meyveler, 4) Ekmek ve tahıllar. "
            "Yetişkin bir birey için günde 2 porsiyon süt grubu yeterli iken, gebelik ve emziklilikte bu ihtiyaç 3-4 porsiyona çıkar.\n\n"
            "> [SINAV SPOTU] Günlük porsiyon önerileri: Süt ve ürünleri yetişkinde 2 porsiyon iken gebe ve emziklide 3-4 PORSİYON; "
            "Et, tavuk, balık, yumurta grubu yetişkinde 2 iken gebe ve emziklide 3 PORSİYON tüketilmelidir.\n\n"
            "Sebze ve meyve grubu antioksidan vitaminler ve kabızlığı önleyen posayı sağlarken; tahıllar enerjiyi temin eder ancak "
            "gebelikte tahıl porsiyonunun artırılmasına gerek yoktur."
        ),
        "medicalTerms": [
            {"term": "Dört Yapraklı Yonca Modeli", "explanation": "Türkiye Beslenme Rehberi'nde süt, et, sebze-meyve ve tahıl gruplarını simgeleyen dengeli beslenme modelidir."},
            {"term": "Süt Grubu Porsiyonu", "explanation": "1 kupa süt (200 ml), 1 kase yoğurt (200 g) veya 2 dilim peynirin (60 g) temsil ettiği ölçüdür."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Süt ve ürünleri: Yetişkinde 2 porsiyon; gebe ve emziklide 3 - 4 porsiyon.",
            "📌 [SINAV SPOTU] Et, yumurta, baklagil: Yetişkinde 2 porsiyon; gebe ve emziklide 3 porsiyon.",
            "📌 [SINAV SPOTU] Gebelikte ek tahıl porsiyonuna gerek yoktur (emziklilikte +1,5 porsiyon gerekecektir)."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Süt: 3-4 Porsiyon", "desc": "Kalsiyum ve fosfor ihtiyacı için porsiyon katlanır.", "isKey": True},
                {"title": "Et: 3 Porsiyon", "desc": "Demir, çinko ve B12 vitamini ihtiyacını karşılar.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Türkiye Beslenme Rehberi'ne göre süt ve ürünleri grubu yetişkinde 2 porsiyon iken gebe ve emzikli kadında 3-4 porsiyon olmalıdır.",
                "3-4 porsiyon",
                "Gebede önerilen süt grubu porsiyon adedi"
            ),
            make_active_recall(
                "Türkiye Beslenme Rehberi'ne göre yetişkin kadın ile gebe/emzikli kadının süt grubu ve et grubu günlük porsiyon önerileri nasıldır?",
                "Süt grubu: Yetişkinde 2 porsiyon iken gebe/emziklide 3-4 porsiyondur. Et grubu: Yetişkinde 2 porsiyon iken gebe/emziklide 3 porsiyondur."
            )
        ]
    })

    return slides
