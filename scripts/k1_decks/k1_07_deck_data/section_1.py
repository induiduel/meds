"""
Bölüm 1: Hücre İçi Birikim Mekanizmaları ve Hücresel Lokalizasyon
Adımlar: 1 - 10
Checkpoint: Adım 9 (3 Akıl Kartı)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_1_slides():
    slides = []

    # ADIM 1
    slides.append({
        "slideNumber": 1,
        "title": "Hücre İçi Birikim Kavramı ve Patolojik Önemi",
        "subtitle": "Hücrelerin metabolik yük ve stres karşısında madde depolama dinamikleri",
        "badge": "Giriş ve Kavram",
        "badgeColor": "blue",
        "synthesisNarrative": (
            "Hücre içi birikimler (intraselüler akümülasyonlar), hücrelerin fizyolojik veya patolojik koşullar altında "
            "çeşitli endojen ya da eksojen maddeleri anormal miktarlarda sitoplazma, organel veya çekirdeklerinde "
            "toplaması durumudur. Biriken bu maddeler hücreye tamamen zararsız olabileceği gibi, metabolik süreçleri "
            "aksatarak hücre zedelenmesine, fonksiyon kaybına ve nihayetinde ölüme zemin hazırlayabilir.\n\n"
            "> [TEMEL İLKE] Hücre içi biriken maddenin biyolojik etkisi; maddenin niteliğine, birikme hızına, "
            "hücrenin temizleme kapasitesine ve hücresel kompartımanın duyarlılığına doğrudan bağlıdır.\n\n"
            "Patolojik süreçlerde birikim genellikle metabolizma bozukluğu, genetik mutasyonlar, enzim defektleri veya "
            "dışarıdan sindirilemeyen partiküllerin fagositozu sonucunda tetiklenir."
        ),
        "medicalTerms": [
            {"term": "İntraselüler Akümülasyon", "explanation": "Metabolik veya genetik aksaklıklar sonucu hücre içinde anormal madde depolanmasıdır."},
            {"term": "Endojen Madde", "explanation": "Hücrenin kendi biyokimyasal yollarıyla ürettiği fizyolojik moleküllerdir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Hücre içi biriken maddeler zararsız olabileceği gibi ölümcül hücre hasarına da yol açabilir.",
            "📌 [SINAV SPOTU] Birikimler sitoplazma, lizozomlar veya çekirdekte lokalize olabilir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Birikim Dinamiği", "desc": "Hücre içi sentez, alım ve yıkım dengesizliğinden doğar.", "isKey": True},
                {"title": "Klinik Spektrum", "desc": "Sessiz lipofusin birikiminden ölümcül lizozomal hastalıklara uzanır.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Hücrelerin çeşitli maddeleri anormal miktarlarda depolamasına hücre içi birikim adı verilir.",
                "hücre içi birikim",
                "Hücresel akümülasyon tablosunu tanımlayan kavram"
            ),
            make_active_recall(
                "Hücre içi birikimlerin hücre canlılığı üzerindeki iki temel etkisi nedir?",
                "Tamamen zararsız sessiz bir kalıntı olabileceği gibi hücresel fonksiyonu bozarak hücre ölümüne de yol açabilir."
            )
        ]
    })

    # ADIM 2
    slides.append({
        "slideNumber": 2,
        "title": "Birikimlerin Hücresel Lokalizasyonu: Sitoplazma, Lizozom, Çekirdek",
        "subtitle": "Maddelerin depolandığı anatomik kompartımanlar ve patolojik görünümleri",
        "badge": "Hücresel Lokalizasyon",
        "badgeColor": "indigo",
        "synthesisNarrative": (
            "Hücre içi birikintiler temel olarak üç ana kompartımanda yerleşir: sitoplazma (sitozol), membranöz organeller "
            "(özellikle lizozomlar) ve hücre çekirdeği. Yağ damlacıkları gibi lipidler çoğunlukla serbest sitoplazmada "
            "vakuoller halinde bulunurken, hidrolaz eksikliğiyle parçalanamayan kompleks moleküller lizozomlar içinde göllenir.\n\n"
            "> [KLİNİK İPUCU] Glikojen hem sitoplazmada hem de nükleus içinde birikebilir; diyabetik hepatositlerde "
            "izlenen glikojenli vakuollü nükleuslar çekirdek içi birikimin klasik örneğidir.\n\n"
            "Elektron mikroskopisi ve özel histokimyasal boyalar biriken maddenin hangi kompartımanda yer aldığını net "
            "olarak göstererek altta yatan patofizyolojik mekanizmanın aydınlatılmasını sağlar."
        ),
        "medicalTerms": [
            {"term": "Lizozom", "explanation": "Asit hidrolaz enzimleri içeren, hücre içi sindirimden sorumlu organeldir."},
            {"term": "Nükleer Glikojen", "explanation": "Diyabet gibi durumlarda çekirdek içine glikojen infiltrasyonudur."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Enzim eksikliğine bağlı parçalanamayan kompleks substratlar öncelikle lizozomlarda birikir.",
            "📌 [SINAV SPOTU] Serbest trigliserid damlacıkları hepatosit sitoplazmasında vakuol oluşturur."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Sitoplazmik Havuz", "desc": "Lipid damlacıkları, sitozolik protein agregatları ve glikojen granülleri.", "isKey": True},
                {"title": "Lizozomal Havuz", "desc": "Sfingolipidler, glikozaminoglikanlar ve fagositoz atıkları.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Kompartıman", "Tipik Biriken Madde", "Karakteristik Örnek"],
                [
                    [("Sitozol / Sitoplazma", False, ""), ("Trigliserid damlacıkları", True, "Karaciğer parankiminde depolanan nötral lipid"), ("Karaciğer steatozu", False, "")],
                    [("Lizozomlar", False, ""), ("Parçalanamayan sfingolipidler", True, "Hidrolaz eksikliğinde biriken lipid türevi"), ("Tay-Sachs hastalığı", False, "")],
                    [("Nükleus (Çekirdek)", False, ""), ("Glikojen agregatları", True, "Diyabette çekirdekte biriken polisakkarit"), ("Diyabetik hepatosit çekirdeği", False, "")]
                ]
            ),
            make_cloze(
                "Enzim eksikliği sonucu yıkılamayan kompleks metabolitler başlıca lizozomlar organelinde depolanır.",
                "lizozomlar",
                "Asit hidrolazların bulunduğu sindirim organeli"
            )
        ]
    })

    # ADIM 3
    slides.append({
        "slideNumber": 3,
        "title": "Temel Mekanizma 1: Normal Maddenin Yetersiz Uzaklaştırılması",
        "subtitle": "Üretim hızı ile metabolik klirens arasındaki dengesizliğin sonuçları",
        "badge": "Mekanizma 1",
        "badgeColor": "amber",
        "synthesisNarrative": (
            "Hücre içi birikimin birinci temel mekanizması, normal bir endojen maddenin normal veya artmış hızda "
            "üretilmesine rağmen, metabolik uzaklaştırma (klirens, sekresyon veya katabolizma) hızının yetersiz "
            "kalmasıdır. Burada biriken madde moleküler olarak tamamen normaldir; ancak hücrenin taşıma veya işleme "
            "kapasitesi aşılmıştır.\n\n"
            "> [YÜKSEK VERİM] Karaciğer steatozu (yağlanması), hepatositlerde trigliserid sentezinin apolipoproteinlerle "
            "paketlenip VLDL şeklinde kana salgılanma hızını aşması sonucu gelişen en yaygın mekanizma 1 örneğidir.\n\n"
            "Benzer şekilde, nefrotik sendromda idrara kaçan aşırı albüminin böbrek proksimal tübül epiteli tarafından "
            "pinositozla emilmesi ve lizozomal sindirim hızının yetersiz kalması da bu gruba girer."
        ),
        "medicalTerms": [
            {"term": "Steatoz", "explanation": "Parankimal hücrelerde trigliseridlerin aşırı birikmesidir."},
            {"term": "Apolipoprotein", "explanation": "Lipidleri bağlayıp lipoprotein halinde sekresyonunu sağlayan taşıyıcı proteindir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Yağlı karaciğerde biriken trigliserid normal endojen bir maddedir.",
            "📌 [SINAV SPOTU] Hata moleküler yapıda değil, üretim-uzaklaştırma dengesizliğindedir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Normal Madde Prensibi", "desc": "Moleküler yapı bozuk değildir, taşınma ve salgılama yetersizdir.", "isKey": True},
                {"title": "Geri Dönüşümlülük", "desc": "Metabolik yük kalktığında birikinti hücre tarafından tamamen temizlenebilir.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_causal_chain(
                "Steatozda Yetersiz Uzaklaştırma Mekanizması",
                [
                    "1. Yağ Asidi Girişi: Dolaşımdan karaciğere serbest yağ asidi akışı belirgin şekilde artar.",
                    "2. Trigliserid Sentezi: Hepatositler aşırı yağ asitlerini trigliseridlere dönüştürür.",
                    "3. Sekresyon Yetersizliği: Apolipoprotein sentezi yetersiz kalarak VLDL çıkışı bloke olur.",
                    "4. İntraselüler Depolanma: Sitoplazmada lipid vakuolleri birikerek steatoz tablosunu oluşturur."
                ]
            ),
            make_cloze(
                "Yağlı karaciğer gelişiminde biriken trigliseridler normal endojen moleküllerdir.",
                "endojen",
                "Hücrenin kendi metabolizmasında ürettiği iç kaynaklı madde türü"
            )
        ]
    })

    # ADIM 4
    slides.append({
        "slideNumber": 4,
        "title": "Temel Mekanizma 2: Anormal Endojen Maddenin Birikmesi",
        "subtitle": "Genetik mutasyonlar ve katlanma hatalarının neden olduğu proteinopatiler",
        "badge": "Mekanizma 2",
        "badgeColor": "red",
        "synthesisNarrative": (
            "İkinci mekanizma, genetik mutasyonlar veya post-translasyonel katlanma bozuklukları nedeniyle yapısal "
            "olarak anormal bir endojen maddenin üretilmesidir. Normal şaperon sistemleri ve ubikitin-proteazom yolağı "
            "bu hatalı katlanmış polipeptitleri parçalayamaz veya endoplazmik retikulumdan (ER) dışarı taşıyamaz.\n\n"
            "> [KRİTİK UYARI] En çarpıcı model α1-antitripsin (AAT) eksikliğidir; SERPINA1 gen mutasyonu sonucu hepatosit "
            "ER'sinde biriken mutant protein karaciğerde hasar yaparken, kanda eksikliği akciğerde amfizeme yol açar.\n\n"
            "Bu anormal proteinlerin hücre içinde birikmesi şiddetli ER stresine (açılmamış protein yanıtı) yol açar ve "
            "apoptoz mekanizmalarını tetikleyerek parankim kaybını hızlandırır."
        ),
        "medicalTerms": [
            {"term": "α1-Antitripsin", "explanation": "Karaciğerde üretilen ve nötrofil elastazını inhibe eden koruyucu proteaz inhibitörüdür."},
            {"term": "ER Stresi", "explanation": "Hatalı katlanmış proteinlerin ER lümeninde birikmesiyle tetiklenen hücresel stres yanıtıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] SERPINA1 gen mutasyonu mutant α1-antitripsin proteininin hepatosit ER'sinde birikmesine yol açar.",
            "📌 [SINAV SPOTU] Katlanma bozukluğu proteazom yıkımından kaçarak intraselüler agregat oluşturur."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Mutant Molekül", "desc": "Genetik mutasyon proteinin üçüncül yapısını bozar.", "isKey": True},
                {"title": "Çift Yönlü Patoloji", "desc": "Karaciğerde toksik birikim, hedef organda (akciğer) fonksiyonel eksiklik.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_micro_quiz(
                "Aşağıdakilerden hangisi anormal endojen madde birikimi mekanizmasına en uygun patolojik örnektir?",
                {
                    "A": "Hava kirliliğine bağlı akciğer makrofajlarında karbon birikimi",
                    "B": "SERPINA1 mutasyonuna bağlı hepatositlerde mutant α1-antitripsin depolanması",
                    "C": "Aşırı alkol alımına bağlı hepatositlerde trigliserid birikimi",
                    "D": "Tay-Sachs hastalığında lizozomlarda gangliozid birikimi",
                    "E": "Tüberküloz odağında distrofik kalsiyum çökmesi"
                },
                "B",
                {
                    "A": "Karbon partikülleri eksojen anormal madde birikimi (mekanizma 3) örneğidir.",
                    "B": "Mutant α1-antitripsin yanlış katlanan anormal endojen protein birikiminin klasik örneğidir.",
                    "C": "Steatoz normal endojen maddenin yetersiz uzaklaştırılması (mekanizma 1) grubundadır.",
                    "D": "Tay-Sachs lizozomal enzim eksikliği (mekanizma 4) tablosudur.",
                    "E": "Kalsiyum çökmesi distrofik kalsifikasyon olup hücre dışı/içi mineral birikimidir."
                }
            ),
            make_cloze(
                "Mutant α1-antitripsin moleküllerinin hepatositlerin endoplazmik retikulum organelinde göllenmesi ER stresine yol açar.",
                "endoplazmik retikulum",
                "Proteinlerin katlandığı ve taşındığı granüllü membran sistemi"
            )
        ]
    })

    # ADIM 5
    slides.append({
        "slideNumber": 5,
        "title": "Temel Mekanizma 3: Eksojen Anormal Maddenin Alınması ve Birikimi",
        "subtitle": "Hücrenin metabolize edemediği dış kaynaklı parçacıkların fagositozu",
        "badge": "Mekanizma 3",
        "badgeColor": "stone",
        "synthesisNarrative": (
            "Hücre içi birikimlerin üçüncü temel mekanizması, hücrenin parçalayacak enzimatik donanıma veya taşıyacak "
            "taşıma sistemine sahip olmadığı eksojen (dış kaynaklı) bir maddeyi içeri almasıdır. Bu yabancı partiküller "
            "genellikle fagositoz yoluyla makrofajlar tarafından yutulur ve lizozomlara aktarılır.\n\n"
            "> [SINAV SPOTU] Karbon partikülleri (kömür tozu) en sık karşılaşılan eksojen maddedir; akciğer alveoler "
            "makrofajlarında birikerek antrakozis tablosunu oluşturur.\n\n"
            "Diğer önemli eksojen ajanlar arasında silika kristalleri, asbest lifleri ve dövme (tattoo) pigmentleri yer alır. "
            "Enzimler bu mineral ve inorganik maddeleri sindiremediği için birikim ömür boyu kalıcı olabilir."
        ),
        "medicalTerms": [
            {"term": "Antrakozis", "explanation": "Akciğer parankimi ve hiler lenf nodlarında karbon pigmenti depolanmasıdır."},
            {"term": "Eksojen Madde", "explanation": "Vücut dışından solunum, sindirim veya parenteral yolla alınan maddelerdir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Hücre eksojen inorganik maddeleri parçalayacak hidrolitik enzimlere sahip değildir.",
            "📌 [SINAV SPOTU] Karbon pigmenti alveoler makrofajların fagozomlarında birikir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Sindirilemeyen Yabancı Madde", "desc": "Biyolojik yıkım yolları inorganik kristalleri etkisiz kılamaz.", "isKey": True},
                {"title": "Doku Reaksiyonu", "desc": "Karbon genellikle inerttir; silika ve asbest ise şiddetli fibrozise yol açar.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "Karbon (İnert) vs Silika (Fibrojenik) Eksojen Partiküller",
                "Antrakozis (Karbon)",
                "Alveoler makrofajlarda biriken karbon genellikle doku hasarı yapmadan sessiz siyah pigmentasyon olarak kalır.",
                "Silikozis (Silika)",
                "Makrofaj membranlarını parçalayarak inflamatuvar mediyatörleri salar ve ilerleyici pulmoner fibrozise neden olur."
            ),
            make_active_recall(
                "Hücrelerin eksojen maddeleri parçalayamamasının temel biyokimyasal nedeni nedir?",
                "Hücrelerin inorganik mineralleri veya karbon kristallerini parçalayabilecek özgül enzim sistemlerine sahip olmamasıdır."
            )
        ]
    })

    # ADIM 6
    slides.append({
        "slideNumber": 6,
        "title": "Temel Mekanizma 4: Lizozomal Enzim Eksikliği ve Depo Hastalıkları",
        "subtitle": "Genetik hidrolaz defektleri ve ara metabolitlerin lizozomal göllenmesi",
        "badge": "Mekanizma 4",
        "badgeColor": "purple",
        "synthesisNarrative": (
            "Dördüncü mekanizma, kalıtsal enzim eksikliği nedeniyle lizozomlarda substratların tam olarak parçalanamaması "
            "ve kısmen sindirilmiş metabolitlerin organel içinde birikmesidir. Bu patolojiler lizozomal depo hastalıkları "
            "(LSD) üst başlığında toplanır ve çoğunlukla otozomal resesif geçiş gösterir.\n\n"
            "> [YÜKSEK VERİM] Eksik olan özgül hidrolaz enzimi nedeniyle substrat (örneğin sfingolipid veya "
            "mukopolisakkarit) lizozomda birikir; lizozomlar şişerek hücre hacmini genişletir ve hücresel mimariyi bozar.\n\n"
            "Bu durum nöronlarda dejenerasyona, hepatosplenomegaliye, iskelet deformitelerine ve erken çocukluk "
            "çağında ölümcül multisistemik tutulumlara yol açabilir."
        ),
        "medicalTerms": [
            {"term": "Lizozomal Depo Hastalığı", "explanation": "Lizozom hidrolaz enzimlerinin genetik yokluğunda substrat depolanmasıyla giden kalıtsal hastalıklardır."},
            {"term": "Asit Hidrolaz", "explanation": "Lizozomun asidik lümeninde (pH 4.5-5.0) aktif olan sindirim enzimleridir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Lizozomal depo hastalıklarının temelinde mutasyona bağlı özgül hidrolaz enzim eksikliği yatar.",
            "📌 [SINAV SPOTU] Substrat birikimi öncelikle lizozom lümeninde başlar ve organeli şişirir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Enzim Defekti", "desc": "Tek bir hidrolazın eksikliği karmaşık lipid veya şeker yıkımını bloke eder.", "isKey": True},
                {"title": "Organel Şişmesi", "desc": "Lizozomlar hücre sitoplazmasını doldurarak organel fonksiyonlarını kilitler.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_cloze(
                "Kalıtsal hidrolaz enzim eksikliği sonucu parçalanamayan metabolitlerin organelde göllenmesine lizozomal depo hastalıkları denir.",
                "lizozomal depo hastalıkları",
                "Enzim yokluğunda substrat göllenmesiyle giden kalıtsal metabolik hastalık grubu"
            ),
            make_branching_logic(
                "Bir çocuk hastada hepatosplenomegali ve ilerleyici nörolojik gerileme saptanıyor. Karaciğer biyopsisinde sitoplazması şişkin lizozomlarla dolu hücreler izleniyor.",
                [
                    {
                        "text": "Karbon partiküllerine bağlı eksojen pigment birikimi düşünülmelidir.",
                        "isCorrect": False,
                        "feedback": "Karbon partikülleri eksojen kökenlidir ve nörolojik gerileme veya lizozomal enzim eksikliği yapmaz."
                    },
                    {
                        "text": "Lizozomal hidrolaz eksikliğine bağlı depo hastalığı düşünülmeli ve enzim analizi yapılmalıdır.",
                        "isCorrect": True,
                        "feedback": "Doğru karar! Çocukluk çağındaki nörodejenerasyon ve şişkin lizozomlar lizozomal depo hastalığını işaret eder."
                    }
                ]
            )
        ]
    })

    # ADIM 7
    slides.append({
        "slideNumber": 7,
        "title": "Lizozomal Depo Hastalıkları: Sfingolipidozlar ve Mukopolisakkaridozlar",
        "subtitle": "Tay-Sachs, Niemann-Pick ve Gaucher patolojilerinin karşılaştırmalı moleküler profili",
        "badge": "Depo Hastalıkları",
        "badgeColor": "teal",
        "synthesisNarrative": (
            "Lizozomal depo hastalıkları biriken biyokimyasal substratın kimyasal yapısına göre sınıflandırılır. "
            "Sfingolipidozlar grubunda Tay-Sachs hastalığı heksozaminidaz A enzim eksikliğine bağlı GM2 gangliozid "
            "birikimiyle seyreder ve santral sinir sistemini yıkar. Niemann-Pick sfingomiyelinaz eksikliğiyle, "
            "Gaucher hastalığı ise glukoserebrozidaz eksikliğiyle karakterizedir.\n\n"
            "> [KLİNİK İPUCU] Mukopolisakkaridozlarda (Hurler, Hunter) heparan ve dermatan sülfat gibi glikozaminoglikanlar "
            "yıkılamaz; kaba yüz görünümü, korneal bulanıklık ve kalp kapak tutulumu gelişir.\n\n"
            "Bu hastalıklarda patolog doku kesitlerinde 'köpüksü sitoplazmalı' makrofajlar (örneğin Gaucher hücreleri "
            "buruşuk kağıt görünümündedir) ve aşırı büyümüş lizozomal vakuoller tespit eder."
        ),
        "medicalTerms": [
            {"term": "Tay-Sachs", "explanation": "Heksozaminidaz A eksikliğinde GM2 gangliozid biriken nörodejeneratif hastalıktır."},
            {"term": "Gaucher Hücresi", "explanation": "Glukoserebrozid birikimiyle sitoplazması buruşuk kağıt görünümü alan makrofajdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Tay-Sachs hastalığında eksik enzim heksozaminidaz A, biriken madde GM2 ganglioziddir.",
            "📌 [SINAV SPOTU] Niemann-Pick hastalığında sfingomiyelin, Gaucher hastalığında glukoserebrozid birikir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Sfingolipidozlar", "desc": "Nöron ve RES makrofajlarında lipid türevleri depolanır.", "isKey": True},
                {"title": "Mukopolisakkaridozlar", "desc": "Kıkırdak, bağ doku ve damarlarda sülfatlı şekerler birikir.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_table(
                ["Hastalık", "Eksik Enzim", "Biriken Temel Substrat"],
                [
                    [("Tay-Sachs Hastalığı", False, ""), ("Heksozaminidaz A", True, "Eksik alfa alt birimi enzimi"), ("GM2 Gangliozid", False, "")],
                    [("Niemann-Pick Hastalığı", False, ""), ("Sfingomiyelinaz", True, "Sfingomiyelini yıkan lizozomal enzim"), ("Sfingomiyelin", False, "")],
                    [("Gaucher Hastalığı", False, ""), ("Glukoserebrozidaz", True, "Glukozilseramidi yıkan hidrolaz"), ("Glukoserebrozid", False, "")]
                ]
            ),
            make_cloze(
                "Tay-Sachs hastalığında lizozomal hidrolaz eksikliği nedeniyle nöronlarda GM2 gangliozid molekülleri depolanır.",
                "GM2 gangliozid",
                "Tay-Sachs'ta biriken kompleks glikolipid substrat"
            )
        ]
    })

    # ADIM 8
    slides.append({
        "slideNumber": 8,
        "title": "Hücre İçi ve Hücre Dışı Birikimlerin Karşılaştırmalı Dinamiği",
        "subtitle": "İntraselüler depolanmalar ile ekstraselüler matriks birikintilerinin ayrımı",
        "badge": "Karşılaştırma",
        "badgeColor": "cyan",
        "synthesisNarrative": (
            "Patolojik süreçlerde birikintiler yalnızca hücrelerin sitoplazmasında toplanmaz; hücre dışı matrikste de "
            "belirgin madde depolanmaları meydana gelebilir. Hücre içi birikimler (steatoz, lizozomal birikimler, "
            "Russell cisimcikleri) hücre bütünlüğünü doğrudan etkileyip organel disfonksiyonu yaratırken; hücre dışı "
            "birikimler interstisyel doku mimarisini ve kılcal damar geçirgenliğini bozar.\n\n"
            "> [YÜKSEK VERİM] Hücre dışı birikimlerin en tipik örnekleri amiloid lifleri, hiyalinize skarlar ve "
            "patolojik kalsiyum tuzlarıdır.\n\n"
            "Örneğin aterosklerozda kolesterol başlangıçta makrofaj ve düz kas hücresi içinde (köpük hücre) toplanırken, "
            "hücrelerin parçalanmasıyla ekstraselüler kristalize kolesterol yarıkları ve matriks kalsifikasyonu gelişir."
        ),
        "medicalTerms": [
            {"term": "Hücre Dışı Matriks", "explanation": "Hücreleri çevreleyen, kollajen, proteoglikan ve glikoproteinlerden oluşan destek yapıdır."},
            {"term": "Amiloid", "explanation": "Hücreler arasında beta kırmalı yapıda biriken patolojik fibriler proteindir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Amiloid ve patolojik kalsifikasyon öncelikle hücre dışı matrikste birikinti oluşturur.",
            "📌 [SINAV SPOTU] Aterosklerotik lezyonlar hem hücre içi hem hücre dışı lipid depolanması içerir."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Hücre İçi Odak", "desc": "Hücresel metabolizmayı ve organel taşınmasını kilitler.", "isKey": True},
                {"title": "Hücre Dışı Odak", "desc": "Doku esnekliğini azaltır, damarları tıkar ve difüzyonu engeller.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_before_after(
                "Hücre İçi Birikimler vs Hücre Dışı Birikimler",
                "Hücre İçi Birikimler",
                "Sitoplazma, lizozom veya çekirdekte toplanır; metabolik bozukluk, ER stresi veya fagositoz ile ilişkilidir.",
                "Hücre Dışı Birikimler",
                "İnterstisyel alanda ve bağ dokusunda toplanır; amiloidoz, hiyalinize skar ve distrofik kalsiyum birikimini kapsar."
            ),
            make_active_recall(
                "Aterosklerozda lipid birikimi hücre içi ve hücre dışı kompartımanlarda nasıl dağılır?",
                "Erken dönemde makrofaj ve düz kas hücresi içinde köpük hücreler halinde, ileri evrede hücre lizisiyle ekstraselüler kristaller halinde bulunur."
            )
        ]
    })

    # ADIM 9 - CHECKPOINT 1
    slides.append({
        "slideNumber": 9,
        "title": "[TEKRAR SAYFASI - CHECKPOINT 1] Hücre İçi Birikim Mekanizmaları ve Lokalizasyon",
        "subtitle": "Dört temel birikim mekanizması ve hücresel kompartımanların sentezi",
        "badge": "Checkpoint",
        "badgeColor": "red",
        "isCheckpoint": True,
        "checkpointNumber": 1,
        "synthesisNarrative": (
            "Bu checkpoint sayfasında hücre içi birikimlerin 4 temel mekanizmasını ve hücresel lokalizasyon kurallarını "
            "pekiştiriyoruz. Dört temel mekanizma: 1) Normal endojen maddenin yetersiz uzaklaştırılması (karaciğer "
            "steatozu), 2) Anormal endojen maddenin birikmesi ve ER stresi (mutant α1-antitripsin), 3) Eksojen anormal "
            "maddenin fagositozu (karbon/antrakozis), 4) Lizozomal hidrolaz eksikliği sonucu substrat depolanması "
            "(Tay-Sachs, Gaucher, Niemann-Pick).\n\n"
            "> [KRİTİK UYARI] Sınavda sorulan vakanın mekanizmasını belirlerken maddenin kaynağını (iç/dış), moleküler "
            "yapısını (normal/mutant) ve hücrenin temizleme mekanizmasını mutlaka adım adım sorgulayınız.\n\n"
            "Aşağıdaki 3 akıl kartını dikkatle gözden geçirerek temel mekanizmaları zihninize sabitleyiniz."
        ),
        "medicalTerms": [
            {"term": "Hücre İçi Birikim", "explanation": "Metabolik veya genetik defekt sonucu hücre kompartımanlarında madde depolanmasıdır."},
            {"term": "ER Açılmamış Protein Yanıtı", "explanation": "Hatalı katlanan proteinlerin ER'de birikmesiyle indüklenen koruyucu ve apoptotik sinyal ağıdır."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Dört mekanizmanın ayrımı sınav sorularının en temel omurgasıdır.",
            "📌 [SINAV SPOTU] Enzim eksikliği lizozomal birikime, mutant proteinler ER stresine yol açar."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Mekanizma 1", "desc": "Normal madde, yetersiz klirens (steatoz).", "isKey": True},
                {"title": "Mekanizma 2", "desc": "Anormal madde, katlanma hatası (α1-antitripsin).", "isKey": True},
                {"title": "Mekanizma 3", "desc": "Eksojen madde, sindirilemeyen partikül (karbon).", "isKey": True},
                {"title": "Mekanizma 4", "desc": "Lizozomal hidrolaz eksikliği (LSD).", "isKey": True}
            ]
        },
        "flashcards": [
            make_flashcard(
                "k1-07-fc-01",
                "Hücre içi birikimlerin 4 temel mekanizması nelerdir?",
                "1) Normal endojen maddenin yetersiz uzaklaştırılması, 2) Anormal endojen maddenin birikmesi, 3) Eksojen anormal maddenin alınması, 4) Lizozomal enzim eksikliği.",
                "Dersin temel 4 maddelik mekanizma tablosu"
            ),
            make_flashcard(
                "k1-07-fc-02",
                "α1-Antitripsin eksikliğinde karaciğer hasarına yol açan mekanizma nedir?",
                "SERPINA1 gen mutasyonu nedeniyle yanlış katlanan mutant proteinin hepatosit endoplazmik retikulumunda birikmesi ve ER stresini tetiklemesidir.",
                "Hatalı katlanan protein ve organel hasarı"
            ),
            make_flashcard(
                "k1-07-fc-03",
                "Antrakozis tablosu hangi birikim mekanizmasının klasik örneğidir?",
                "Eksojen anormal maddenin hücre tarafından alınıp sindirilememesi (Mekanizma 3) örneğidir.",
                "Hava kirliliği ve karbon partikülü fagositozu"
            )
        ],
        "interactiveElements": [
            make_cloze(
                "Kalıtsal hidrolaz defektlerinde substratların parçalanamayarak depolanması lizozomal depo hastalıkları tablosunu oluşturur.",
                "lizozomal depo hastalıkları",
                "Enzim eksikliği sonucu gelişen pediatrik depolanma sendromları"
            )
        ]
    })

    # ADIM 10
    slides.append({
        "slideNumber": 10,
        "title": "Bölüm Sentezi ve Klinik Değerlendirme Senaryosu",
        "subtitle": "Klinik patoloji korelasyonu ve ayırıcı tanı algoritması",
        "badge": "Klinik Sentez",
        "badgeColor": "emerald",
        "synthesisNarrative": (
            "Hücre içi birikim mekanizmalarını klinikte değerlendiren bir hekim veya patolog şu üç temel soruyu sorar: "
            "1) Biriken maddenin kimyasal yapısı nedir (lipid, protein, glikojen, inorganik mineral)? 2) Birikim hangi "
            "hücresel kompartımanda toplanmıştır (sitozol, lizozom, ER, çekirdek)? 3) Hücre canlılığı ve organ fonksiyonu "
            "üzerindeki nihai etkisi nedir?\n\n"
            "> [KLİNİK İPUCU] Birikintinin geri dönüşümlü olup olmaması klinik tedavi stratejisini belirler; örneğin "
            "alkolün kesilmesiyle steatoz gerilerken, lizozomal depo hastalıklarında enzim replasmanı şarttır.\n\n"
            "Bu sistematik yaklaşım, lipid birikimlerinden yanlış katlanmış protein agregatlarına ve pigment depolanmalarına "
            "kadar tüm patolojilerin doğru teşhis edilmesini sağlar."
        ),
        "medicalTerms": [
            {"term": "Ayırıcı Tanı", "explanation": "Benzer klinik ve morfolojik bulgulara sahip hastalıkların elenerek doğru tanıya ulaşılmasıdır."},
            {"term": "Geri Dönüşümlülük", "explanation": "Hücresel hasar oluşturan stres faktörü kalktığında dokunun normale dönebilme yeteneğidir."}
        ],
        "spotPearls": [
            "📌 [SINAV SPOTU] Patolojide temel sorular: Madde nedir, neden birikmiştir ve sonal etkisi nedir?",
            "📌 [SINAV SPOTU] Erken dönemdeki birikintiler çoğunlukla etken ortadan kalktığında geri dönüşümlüdür."
        ],
        "coreContent": {
            "keyBullets": [
                {"title": "Klinik Algoritma", "desc": "Morfolojik saptama, histokimyasal analiz, fonksiyonel değerlendirme.", "isKey": True},
                {"title": "Tedavi Yanıtı", "desc": "Geri dönüşümlü yüklerin temizlenmesi organ yetmezliğini önler.", "isKey": True}
            ]
        },
        "interactiveElements": [
            make_branching_logic(
                "Bir hastada karaciğer biyopsisinde hepatosit sitoplazmasında geniş lipid vakuolleri izleniyor. Hastanın obezite ve kontrolsüz tip 2 diyabeti mevcut. Patolog tanıyı nasıl yapılandırmalıdır?",
                [
                    {
                        "text": "Anormal eksojen madde birikimine bağlı antrakozis tanısı konulmalıdır.",
                        "isCorrect": False,
                        "feedback": "Antrakozis akciğerde karbon birikimidir; karaciğerdeki lipid depolanması steatozdur."
                    },
                    {
                        "text": "Normal endojen maddenin (trigliserid) yetersiz uzaklaştırılmasına bağlı karaciğer steatozu tanısı konulmalıdır.",
                        "isCorrect": True,
                        "feedback": "Mükemmel! Diyabet ve obezitede artan serbest yağ asitleri karaciğerde trigliserid birikimi (steatoz) oluşturur."
                    }
                ]
            ),
            make_active_recall(
                "Patolog hücre içi birikintiyi değerlendirirken hangi 3 temel sorunun yanıtını arar?",
                "Biriken madde nedir, neden birikmiştir ve hücre veya organda neye yol açmaktadır sorularını arar."
            )
        ]
    })

    return slides
